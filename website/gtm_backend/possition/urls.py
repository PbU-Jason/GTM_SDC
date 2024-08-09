from django.urls import path
from . import views

urlpatterns = [
    path('', views.now_lon_lat, name='now_lon_lat'),
]
