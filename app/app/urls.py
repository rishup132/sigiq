from django.urls import path
from . import views
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)

urlpatterns = [
    path("version/", views.version),
    path("healthz/", views.health),
    path("metrics/", metrics_view),
]