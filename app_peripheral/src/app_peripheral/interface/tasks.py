from celery import current_task, shared_task


@shared_task()
def local_celery_task(body):
    print(f"From the executed task: {body} (on app_peripheral)")
    return body


@shared_task()
def crossover_task(body):
    exchange = current_task.request.delivery_info.get("exchange")
    routing_key = current_task.request.delivery_info.get("routing_key")
    queue = current_task.request.delivery_info.get("routing_key")
    print(
        f"-- From the executed task: {body} (on app_peripheral, from app_core)  {exchange=},  {routing_key=}, {queue=}"
    )
    return body
