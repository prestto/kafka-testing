from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("This is app_core")
