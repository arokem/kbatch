from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django_kbatch_server import views


router = routers.DefaultRouter()
router.register(r"jobs", views.JobViewSet)
router.register(r"uploads", views.UploadViewSet)

urlpatterns = [
    path(settings.JUPYTERHUB_SERVICE_PREFIX, include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]


if settings.JUPYTERHUB_SERVICE_PREFIX:
    # ignoring this:
    # kbatch-server/kbatch_server/urls.py:20: error: Argument 1 to "append" of "list"
    # has incompatible type "URLPattern"; expected "URLResolver"
    urlpatterns.append(path("", views.root))  # type: ignore
