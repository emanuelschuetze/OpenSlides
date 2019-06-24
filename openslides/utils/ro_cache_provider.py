import asyncio
import functools
import hashlib
from collections import defaultdict
from textwrap import dedent
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, Tuple

from django.conf import settings

from . import logging
from .cache_providers import CacheReset, ElementCacheProvider
from .redis import aioredis, get_connection
from .schema_version import SchemaVersion
from .utils import split_element_id


logger = logging.getLogger(__name__)
CACHE_RETRY_TIME = getattr(settings, "CACHE_RETRY_TIME", 10)  # seconds
logger.info(f"CACHE_RETRY_TIME={CACHE_RETRY_TIME}")


class ShouldNotBeUsed(Exception):
    pass


def wait_inmemory_data_wrapper() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    """

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapped(
            cache_provider: ElementCacheProvider, *args: Any, **kwargs: Any
        ) -> Any:
            success = False
            while not success:
                try:
                    result = await func(cache_provider, *args, **kwargs)
                    success = True
                except CacheReset:
                    logger.warn(
                        f"Redis was flushed before method '{func.__name__}'. Retry in {CACHE_RETRY_TIME} seconds."
                    )
                    await asyncio.sleep(CACHE_RETRY_TIME)
            return result

        return wrapped

    return wrapper


class RedisMemoryCacheProvider:
    """
    This is a mixture of the RedisCacheProvider and MemoryCacheProvider...
    """

    get_full_data_script = dedent(
        """
        local exist = redis.call('exists', KEYS[1])
        if (exist == 0) then
            redis.log(redis.LOG_WARNING, "empty: "..KEYS[1])
            return redis.error_reply("cache_reset")
        end
        return redis.call('hgetall', KEYS[1])
    """
    )

    full_data_key = "full_data"
    change_id_key = "change_id"
    schema_key = "schema"

    def __init__(self, ensure_cache: Callable[[], Coroutine[Any, Any, None]]) -> None:
        # hash all scripts and remove indentation.
        self.get_full_data_script_hash = hashlib.sha1(
            self.get_full_data_script.encode()
        ).hexdigest()
        self.set_data_dicts()

    def set_data_dicts(self) -> None:
        self.full_data: Dict[bytes, bytes] = {}
        self.change_id_data: Dict[int, Set[str]] = {}
        self.schema_version: Optional[SchemaVersion] = None
        self.default_change_id: int = -1

    async def sync(self):
        # Save olf change id values
        old_lowest_change_id = self.default_change_id
        if self.change_id_data:
            old_current_change_id = max(self.change_id_data.keys())
        else:
            old_current_change_id = self.default_change_id

        self.set_data_dicts()  # reset

        # First, get all change ids
        async with get_connection() as redis:
            changed_element_pairs = await redis.zrangebyscore(
                self.change_id_key, withscores=True
            )

        current_change_id = 0
        for element_id, change_id in changed_element_pairs:
            if element_id == b"_config:lowest_change_id":
                self.default_change_id = change_id  # set lowest change id
            if element_id.startswith(b"_config"):
                # Ignore config values from the change_id cache key
                continue
            if change_id in self.change_id_data:
                self.change_id_data[change_id].add(element_id.decode())
            else:
                self.change_id_data[change_id] = {element_id.decode()}
            if change_id > current_change_id:
                current_change_id = change_id

        # 2) Get full data
        self.full_data = await aioredis.util.wait_make_dict(
            self.eval(
                self.get_full_data_script,
                self.get_full_data_script_hash,
                [self.full_data_key],
            )
        )

        # 3) get schema
        async with get_connection() as redis:
            schema_version = await redis.hgetall(self.schema_key)
        if schema_version:
            self.schema_version = {
                "migration": int(schema_version[b"migration"].decode()),
                "config": int(schema_version[b"config"].decode()),
                "db": schema_version[b"db"].decode(),
            }
        else:
            self.schema_version = None

        logger.info(
            f"SYNC DONE: lowest_change_id from {old_lowest_change_id} to {self.default_change_id};"
            + f" current_change_id from {old_current_change_id} to {current_change_id}"
        )

    async def eval(
        self, script: str, hash: str, keys: List[str] = [], args: List[Any] = []
    ) -> Any:
        """
        Runs a lua script in redis. This wrapper around redis.eval tries to make
        usage of redis script cache. First the hash is send to the server and if
        the script is not present there (NOSCRIPT error) the actual script will be
        send.
        If the script uses the ensure_cache-prefix, the first key must be the full_data
        cache key. This is checked here.
        """
        async with get_connection() as redis:
            try:
                return await redis.evalsha(hash, keys, args)
            except aioredis.errors.ReplyError as e:
                if str(e).startswith("NOSCRIPT"):

                    try:
                        return await redis.eval(script, keys, args)
                    except aioredis.errors.ReplyError as e2:
                        if str(e2) == "cache_reset":
                            raise CacheReset()
                        else:
                            raise e2

                elif str(e) == "cache_reset":
                    raise CacheReset()
                else:
                    raise e

    def assert_inmemory_data_exists(self):
        if not bool(self.full_data) or self.default_change_id < 0:
            raise CacheReset()

    @wait_inmemory_data_wrapper()
    async def get_all_data(self) -> Dict[bytes, bytes]:
        self.assert_inmemory_data_exists()
        return self.full_data  # TODO: We should not need to copy this..

    @wait_inmemory_data_wrapper()
    async def get_collection_data(self, collection: str) -> Dict[int, bytes]:
        self.assert_inmemory_data_exists()

        out = {}
        query = f"{collection}:"
        for element_id, value in self.full_data.items():
            if element_id.decode().startswith(query):
                _, id = split_element_id(element_id)
                out[id] = value
        return out

    @wait_inmemory_data_wrapper()
    async def get_element_data(self, element_id: str) -> Optional[bytes]:
        self.assert_inmemory_data_exists()

        value = self.full_data.get(element_id.encode(), None)
        return value

    @wait_inmemory_data_wrapper()
    async def get_data_since(
        self, change_id: int, max_change_id: int = -1
    ) -> Tuple[Dict[str, List[bytes]], List[str]]:
        self.assert_inmemory_data_exists()

        changed_elements: Dict[str, List[bytes]] = defaultdict(list)
        deleted_elements: List[str] = []

        all_element_ids: Set[str] = set()
        for data_change_id, element_ids in self.change_id_data.items():
            if data_change_id >= change_id and (
                max_change_id == -1 or data_change_id <= max_change_id
            ):
                all_element_ids.update(element_ids)

        for element_id in all_element_ids:
            element_json = self.full_data.get(element_id.encode(), None)
            if element_json is None:
                deleted_elements.append(element_id)
            else:
                collection_string, id = split_element_id(element_id)
                changed_elements[collection_string].append(element_json)
        return changed_elements, deleted_elements

    @wait_inmemory_data_wrapper()
    async def get_current_change_id(self) -> Optional[int]:
        self.assert_inmemory_data_exists()

        if self.change_id_data:
            return max(self.change_id_data.keys())
        else:
            return await self.get_lowest_change_id()

    @wait_inmemory_data_wrapper()
    async def get_lowest_change_id(self) -> Optional[int]:
        self.assert_inmemory_data_exists()
        return self.default_change_id

    @wait_inmemory_data_wrapper()
    async def get_schema_version(self) -> Optional[SchemaVersion]:
        if self.schema_version is None:
            raise CacheReset()
        return self.schema_version

    async def ensure_cache(self) -> None:
        raise ShouldNotBeUsed()

    async def clear_cache(self) -> None:
        raise ShouldNotBeUsed()

    async def data_exists(self) -> bool:
        raise ShouldNotBeUsed()

    async def reset_full_cache(self, data: Dict[str, str]) -> None:
        raise ShouldNotBeUsed()

    async def add_changed_elements(
        self,
        changed_elements: List[str],
        deleted_element_ids: List[str],
        default_change_id: int,
    ) -> int:
        raise ShouldNotBeUsed()

    async def set_lock(self, lock_name: str) -> bool:
        raise ShouldNotBeUsed()

    async def get_lock(self, lock_name: str) -> bool:
        raise ShouldNotBeUsed()

    async def del_lock(self, lock_name: str) -> None:
        raise ShouldNotBeUsed()

    async def set_schema_version(self, schema_version: SchemaVersion) -> None:
        raise ShouldNotBeUsed()
