from django.urls import path
from . import views 
from diferencias_top_app.dash_apps.finished_apps import top_interactivo_diferencia

urlpatterns = [
    path('', views.diferencias_top_app, name='diferencias_top_app')
]