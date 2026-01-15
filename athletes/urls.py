from django.urls import path
from athletes.views import list_athletes, overview, create_athlete

app_name = 'athletes'
urlpatterns = [
    path('', overview, name='overview'),
    path("list/", list_athletes, name='list'),
    path("create/", create_athlete, name='create')
]
