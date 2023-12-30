import json
import traceback

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
            print(f"Launching the command: {body_value}")
            tasks.local_celery_task.delay(body_value)
            return JsonResponse({"message": f"Received body: {body_value}"})
        else:
            return JsonResponse(
                {"error": 'Invalid JSON format. Missing "body" key.'}, status=400
            )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"error": "Unexpected error."}, status=500)
