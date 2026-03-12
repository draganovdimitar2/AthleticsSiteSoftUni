from django.urls import path
from athletes.views import list_athletes, overview, create_athlete, confirm_delete_athlete, update_athlete, \
    create_discipline, update_discipline, delete_discipline, \
    create_age_category, update_age_category, delete_age_category

app_name = 'athletes'
urlpatterns = [
    path('', overview, name='overview'),
    path("list/", list_athletes, name='list'),
    path("create/", create_athlete, name='create'),
    path("update/<int:athlete_id>", update_athlete, name='update'),
    path("delete/<int:athlete_id>", confirm_delete_athlete, name='delete'),
    path("discipline/create/", create_discipline, name='create_discipline'),
    path("discipline/update/<int:pk>/", update_discipline, name='update_discipline'),
    path("discipline/delete/<int:pk>/", delete_discipline, name='delete_discipline'),
    path("age-category/create/", create_age_category, name='create_age_category'),
    path("age-category/update/<int:pk>/", update_age_category, name='update_age_category'),
    path("age-category/delete/<int:pk>/", delete_age_category, name='delete_age_category'),
]
