from django.conf.urls import url

from openslides.core import views as core_views

from . import views


urlpatterns = [
    # Auth
    url(r"^login/$", views.UserLoginView.as_view(), name="user_login"),
    url(r"^logout/$", views.UserLogoutView.as_view(), name="user_logout"),
    url(r"^whoami/$", views.WhoAmIView.as_view(), name="user_whoami"),
    url(r"^setpassword/", core_views.ROErrorView.as_view(), name="RO_error_view"),
    url(r"^reset-password/", core_views.ROErrorView.as_view(), name="RO_error_view"),
    url(
        r"^reset-password-confirm/",
        core_views.ROErrorView.as_view(),
        name="RO_error_view",
    ),
]
