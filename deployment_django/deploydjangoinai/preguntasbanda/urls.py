from django.urls import path
from . import views
from preguntasbanda.dash_apps.finished_apps import top_interactivo


urlpatterns = [
    path('', views.preguntasbanda, name='preguntasbanda'),
    path('', views.index,name='index'),
    path('', views.form_name_view,name='index'),
]
