from celery import shared_task


@shared_task()
def local_celery_task(body):
    print(f"From the executed task: {body}")
    return body
