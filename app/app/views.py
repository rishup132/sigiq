from django.http import JsonResponse
import os

def version(request):
    return JsonResponse({"version": os.environ.get("APP_VERSION", "unknown")})

def health(request):
    return JsonResponse({"status": "ok"})