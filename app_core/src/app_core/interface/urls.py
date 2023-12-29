from django.urls import path

from app_core.interface.views import hello_world

urlpatterns = [
    path("", hello_world, name="hello-world"),
]
