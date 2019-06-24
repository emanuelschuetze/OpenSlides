from django.conf import settings
from django.conf.urls import include, url

from openslides.mediafiles.views import protected_serve

from .core import views as core_views


urlpatterns = [
    # URLs for /media/
    url(
        r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip("/"),
        protected_serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
    # Raise errors on every request to /rest, becuase this is a ReadOnly instance!
    url(r"^rest/", core_views.ROErrorView.as_view(), name="RO_error_view"),
    # Other urls defined by modules and plugins
    url(r"^apps/", include("openslides.urls_apps")),
    # Main entry point for all angular pages.
    # Has to be the last entry in the urls.py
    url(r"^(?P<path>.*)$", core_views.IndexView.as_view(), name="index"),
]
