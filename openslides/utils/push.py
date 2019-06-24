import asyncio
import json
import time
import traceback
from collections import defaultdict

import lz4.frame
from django.conf import settings
from websockets.exceptions import ConnectionClosed

from . import logging
from .autoupdate import AutoupdateFormat
from .cache import element_cache, get_all_cachables
from .cache_providers import CacheReset
from .projector import get_projector_data
from .stats import WebsocketThroughputLogger
from .utils import split_element_id


logger = logging.getLogger(__name__)
PUSH_INTERVAL = getattr(settings, "PUSH_INTERVAL", 60)  # seconds
CONSUMER_GROUP_SIZE = getattr(settings, "CONSUMER_GROUP_SIZE", 10)
CONSUMER_GROUP_DELAY = getattr(settings, "CONSUMER_GROUP_DELAY", 0.1)
CONSUMER_TIMEOUT = getattr(settings, "CONSUMER_TIMEOUT", 10)
COMPRESSION = getattr(settings, "COMPRESSION", True)
logger.info(f"PUSH_INTERVAL={PUSH_INTERVAL}")
logger.info(f"CONSUMER_GROUP_SIZE={CONSUMER_GROUP_SIZE}")
logger.info(f"CONSUMER_GROUP_DELAY={CONSUMER_GROUP_DELAY}")
logger.info(f"CONSUMER_TIMEOUT={CONSUMER_TIMEOUT}")
logger.info(f"COMPRESSION={COMPRESSION}")


class ChangeIdTooHighException(Exception):
    pass


class PushService:
    consumers = {}
    projector_hash = {}
    push_started = False

    def __init__(self):
        self._cachables = None

    @property
    def cachables(self):
        """
        Returns all Cachables as a dict where the key is the collection_string of the cachable.
        """
        # This method is neccessary to lazy load the cachables
        if self._cachables is None:
            self._cachables = {
                cachable.get_collection_string(): cachable
                for cachable in get_all_cachables()
            }
        return self._cachables

    # Consumers must have an _id and a change_id
    async def add_consumer(self, consumer):
        self.consumers[consumer._id] = consumer

    async def remove_consumer(self, consumer):
        if consumer._id in self.consumers:
            del self.consumers[consumer._id]

    def start_push(self):
        logger.info("SETUP")
        if not self.push_started:
            loop = asyncio.get_event_loop()
            loop.create_task(self.push_task())
            self.push_started = True

    async def push_task(self):
        while True:
            try:
                await self._push_task()
            except Exception as e:
                tb = traceback.format_exc()
                logger.critical(f"Error in the push task: {repr(e)}\n{tb}")
                logger.info("Restarting the push-task...")

    async def _push_task(self):
        while True:
            logger.info(f"Next sync and push in {PUSH_INTERVAL} seconds.")
            await asyncio.sleep(PUSH_INTERVAL)

            # Sync the cache
            try:
                await element_cache.cache_provider.sync()
            except CacheReset:
                logger.warn("SYNC: production cache not ready")
                continue

            # Push autoupdates
            if len(self.consumers) > 0:
                await self.push()

    async def push(self):
        logger.info("PUSH")
        start = time.time()
        max_change_id = await element_cache.get_current_change_id()
        lowest_change_id = await element_cache.get_lowest_change_id()
        projector_text_data, projector_bytes_data = (
            await self.get_changed_projector_data()
        )

        all_data_consumers = defaultdict(
            list
        )  # higher than highest or lower than lowest; ordered by user_id
        consumers_by_change_id = defaultdict(
            lambda: defaultdict(list)
        )  # All other consumers, mapped to change ids, than mapped by their user id

        user_ids = set()

        amount_up_to_date_consumers = 0
        amount_consumers = len(self.consumers.values())
        for consumer in self.consumers.values():
            user_ids.add(consumer.user_id)
            # Consumers with change_id == max_change_id+1 are skipped. They are up-to-date.
            change_id = consumer.change_id
            if change_id > 0:
                change_id += 1

            if change_id == max_change_id + 1:
                # The client is up-to-date, so nothing will be done
                # return "no autoupdate; client is up-to-date"
                amount_up_to_date_consumers += 1
            elif change_id > max_change_id or change_id < lowest_change_id:
                all_data_consumers[consumer.user_id].append(consumer)
            else:
                consumers_by_change_id[change_id][consumer.user_id].append(consumer)

        # Do normal changed first:
        if len(consumers_by_change_id.keys()) > 100:
            logger.warn("More than 100 different Change ids. Watch out for RAM-usage")

        amount_autoupdate_consumers = 0
        self.timeouts = 0  # collected globally...
        for change_id, user_id_consumer_mapping in consumers_by_change_id.items():
            # get data for change id
            changed_elements, deleted_element_ids = await element_cache.get_data_since(
                change_id=change_id, max_change_id=max_change_id
            )
            futures = []
            for user_id, consumers in user_id_consumer_mapping.items():
                amount_autoupdate_consumers += len(consumers)
                _changed_elements = {
                    key: [x for x in value] for key, value in changed_elements.items()
                }
                _deleted_element_ids = [x for x in deleted_element_ids]

                await self.handle_user_id(
                    user_id,
                    consumers,
                    _changed_elements,
                    _deleted_element_ids,
                    False,
                    change_id,
                    max_change_id,
                    projector_text_data,
                    projector_bytes_data,
                )
                del _changed_elements
                del _deleted_element_ids

        # Do all data
        futures = []
        changed_elements = await element_cache.get_all_data_list()
        amount_all_data_consumers = 0
        for user_id, consumers in all_data_consumers.items():
            amount_all_data_consumers += len(consumers)
            futures.append(
                self.handle_user_id(
                    user_id,
                    consumers,
                    changed_elements,
                    [],
                    True,
                    0,
                    max_change_id,
                    projector_text_data,
                    projector_bytes_data,
                )
            )
        await asyncio.gather(*futures)

        diff_consumers_amount = amount_consumers - len(self.consumers.values())

        stop = time.time()
        diff = stop - start
        logger.info(
            f"PUSH DONE: took {diff:.2f} seconds to update {amount_consumers} consumers "
            + f"({diff_consumers_amount} diff, {self.timeouts} timeouts) "
            + f"with {len(user_ids)} unique users, {len(consumers_by_change_id.keys())} unique change ids, "
            + f"{amount_up_to_date_consumers} consumers with no changes, "
            + f"{amount_autoupdate_consumers} consumers with normal autoupdate and "
            + f"{amount_all_data_consumers} consumers with full update."
        )

    async def handle_user_id(
        self,
        user_id,
        consumers,
        changed_elements,
        deleted_element_ids,
        all_data,
        change_id,
        max_change_id,
        projector_text_data,
        projector_bytes_data,
    ):
        await element_cache.restrict(changed_elements, deleted_element_ids, user_id)

        # Convert element_ids to dict[str, List[int]]
        deleted_elements = defaultdict(list)
        for element_id in deleted_element_ids:
            collection_string, id = split_element_id(element_id)
            deleted_elements[collection_string].append(id)

        message_content = {
            "type": "autoupdate",
            "content": AutoupdateFormat(
                changed=changed_elements,
                deleted=deleted_elements,
                from_change_id=change_id,
                to_change_id=max_change_id,
                all_data=False,
            ),
        }
        text_data, bytes_data = await self.get_data_from_json(message_content)

        # Group consumers
        for i in range(0, len(consumers), CONSUMER_GROUP_SIZE):
            _consumers = consumers[i : i + CONSUMER_GROUP_SIZE]
            for consumer in _consumers:
                try:
                    await self.send(consumer, text_data, bytes_data)

                    # Ignore listen_projector_ids: To save RAM, just send either no data or all projectors
                    # So we must not serialize the projector data on a per-consumer-basis.
                    if len(consumer.listen_projector_ids) > 0:
                        await self.send(
                            consumer, projector_text_data, projector_bytes_data
                        )
                except asyncio.TimeoutError:
                    self.timeouts += 1
                    logger.info(
                        f"Force disconnect consumer {consumer._id} for timing out..."
                    )
                    try:
                        await self.remove_consumer(consumer)
                        await asyncio.wait_for(
                            consumer.close(), timeout=1
                        )  # Do not block...
                    except Exception:
                        pass  # Ignore errors on close..
                else:
                    consumer.change_id = max_change_id

            if CONSUMER_GROUP_DELAY:
                await asyncio.sleep(CONSUMER_GROUP_DELAY)

        del text_data
        del bytes_data

    async def send(self, consumer, text_data, bytes_data):
        if bytes_data:
            await WebsocketThroughputLogger.send(len(bytes_data))
        if text_data:
            await WebsocketThroughputLogger.send(len(text_data))

        try:
            await asyncio.wait_for(
                consumer.send(text_data=text_data, bytes_data=bytes_data),
                timeout=CONSUMER_TIMEOUT,
            )
        except (ConnectionClosed, RuntimeError):
            await self.remove_consumer(consumer)

    async def get_data_from_json(self, content):
        """ Copied from utils.websocket.AsyncCompressedJsonWebsocketConsumer.send_json """
        text_data = json.dumps(content)
        bytes_data = None  # type: ignore

        b_text_data = text_data.encode("utf-8")
        # uncompressed_len = len(b_text_data)

        if COMPRESSION:
            compressed_data = lz4.frame.compress(b_text_data)
            ratio = len(b_text_data) / len(compressed_data)
            if ratio > 1:
                bytes_data = compressed_data
                text_data = None  # type: ignore

        return (text_data, bytes_data)

    async def get_changed_projector_data(self):
        """
        Get all projector data and calculates the projector data. Returnes just the
        changed data in comparison to an old hash of the json string.
        """
        all_projector_data = await get_projector_data()
        projector_data = {}
        for projector_id, data in all_projector_data.items():
            new_hash = hash(str(data))
            if new_hash != self.projector_hash.get(projector_id):
                projector_data[projector_id] = data
                self.projector_hash[projector_id] = new_hash

        text_data, bytes_data = await self.get_data_from_json(
            {"type": "projector", "content": projector_data}
        )

        return text_data, bytes_data


push_service = PushService()
