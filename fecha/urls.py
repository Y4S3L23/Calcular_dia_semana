from django.urls import path

from . import views

app_name = 'fecha'

urlpatterns = [
    path('', views.calcular_dia, name='calcular_dia'),
]
