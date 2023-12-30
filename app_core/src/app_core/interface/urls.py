from django.urls import path

from app_core.interface.views import hello_world, local_celery_task

urlpatterns = [
    path("", hello_world, name="hello-world"),
    path("local-celery-task", local_celery_task, name="local_celery_task"),
]
