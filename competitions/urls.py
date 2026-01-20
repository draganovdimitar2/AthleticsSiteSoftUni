from django.urls import path
from .views import list_competitions
app_name = 'competitions'

urlpatterns = [
    path('list/', list_competitions, name='list')
]
