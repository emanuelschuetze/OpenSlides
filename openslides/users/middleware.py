from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
    _get_user_session_key,
)
from django.utils.crypto import constant_time_compare
from django.utils.deprecation import MiddlewareMixin

from ..utils.cache import element_cache


def get_user_id(request):
    """
    Return the user model instance associated with the given request session.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    user_id = None
    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path == "CUSTOM":  # TODO: rename, global var.
            # get user from cache

            user_data = async_to_sync(element_cache.get_element_data)(
                "users/user", user_id
            )
            if user_data:
                user_id = user_data["id"]

                # Verify the session
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash, user_data["session_auth_hash"]
                )
                if not session_hash_verified:
                    request.session.flush()
                    user_id = None

    return user_id or 0  # AnonymousUser()


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, "session"), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")

        # request.user_id = SimpleLazyObject(lambda: get_user(request))
        request.user_id = get_user_id(request)
