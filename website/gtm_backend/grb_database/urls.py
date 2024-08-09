from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_table, name='download_table'),
]
