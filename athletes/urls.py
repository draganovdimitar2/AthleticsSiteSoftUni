from django.urls import path
from athletes.views import list_athletes

urlpatterns = [
    path("athletes/", list_athletes, name='list_athletes')
]
