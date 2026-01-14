from django.urls import path
from athletes.views import list_athletes

app_name = 'athletes'
urlpatterns = [
    path("list/", list_athletes, name='list')
]
