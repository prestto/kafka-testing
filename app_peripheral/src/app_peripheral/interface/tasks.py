from celery import shared_task


@shared_task()
def local_celery_task(body):
    print(f"From the executed task: {body} (on app_peripheral)")
    return body


@shared_task()
def crossover_task(body):
    print(f"From the executed task: {body} (on app_peripheral, from app_core)")
    return body
