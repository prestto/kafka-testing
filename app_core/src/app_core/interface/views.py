import json
import traceback

from celery.execute import send_task
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app_core.interface import tasks


def hello_world(request):
    return HttpResponse("This is app_core")


@csrf_exempt
def local_celery_task(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        body_value = data.get("body")
        if body_value is not None:
            tasks.local_celery_task.delay(body_value)
            return JsonResponse(
                {
                    "message": f"Launched task with body: {body_value}",
                    "service": "app_core",
                }
            )
        else:
            return JsonResponse(
                {"error": 'Invalid JSON format. Missing "body" key.'}, status=400
            )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception:
        print(traceback.format_exc())
        return JsonResponse({"error": "Unexpected error."}, status=500)


@csrf_exempt
def remote_celery_task(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        body_value = data.get("body")
        if body_value is not None:
            send_task(
                "app_peripheral.interface.tasks.crossover_task",
                args=[body_value],
                queue="cross_over_app_to_peripheral_queue",
            )
            return JsonResponse(
                {
                    "message": f"Launched task with body: {body_value}",
                    "service": "app_core",
                }
            )
        else:
            return JsonResponse(
                {"error": 'Invalid JSON format. Missing "body" key.'}, status=400
            )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception:
        print(traceback.format_exc())
        return JsonResponse({"error": "Unexpected error."}, status=500)
