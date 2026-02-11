from django.urls import path
from athletes.views import list_athletes, overview, create_athlete, confirm_delete_athlete, update_athlete

app_name = 'athletes'
urlpatterns = [
    path('', overview, name='overview'),
    path("list/", list_athletes, name='list'),
    path("create/", create_athlete, name='create'),
    path("update/<int:athlete_id>", update_athlete, name='update'),
    path("delete/<int:athlete_id>", confirm_delete_athlete, name='delete')
]
