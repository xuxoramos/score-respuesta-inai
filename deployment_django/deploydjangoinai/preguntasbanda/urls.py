from django.urls import path
from . import views 
from preguntasbanda.dash_apps.finished_apps import top_interactivo

urlpatterns = [
    path('', views.preguntasbanda, name='preguntasbanda')
]