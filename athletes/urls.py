from django.urls import path
from rest_framework.routers import DefaultRouter
from athletes.views import OverviewView, ListAthletesView, CreateAthleteView, UpdateAthleteView, DeleteAthleteView, \
    CreateDisciplineView, UpdateDisciplineView, DeleteDisciplineView, \
    CreateAgeCategoryView, UpdateAgeCategoryView, DeleteAgeCategoryView, \
    AthleteViewSet

router = DefaultRouter()
router.register(r'api/athletes', AthleteViewSet, basename='athlete-api')

app_name = 'athletes'
urlpatterns = [
    path('', OverviewView.as_view(), name='overview'),
    path("list/", ListAthletesView.as_view(), name='list'),
    path("create/", CreateAthleteView.as_view(), name='create'),
    path("update/<int:athlete_id>", UpdateAthleteView.as_view(), name='update'),
    path("delete/<int:athlete_id>", DeleteAthleteView.as_view(), name='delete'),
    path("discipline/create/", CreateDisciplineView.as_view(), name='create_discipline'),
    path("discipline/update/<int:pk>/", UpdateDisciplineView.as_view(), name='update_discipline'),
    path("discipline/delete/<int:pk>/", DeleteDisciplineView.as_view(), name='delete_discipline'),
    path("age-category/create/", CreateAgeCategoryView.as_view(), name='create_age_category'),
    path("age-category/update/<int:pk>/", UpdateAgeCategoryView.as_view(), name='update_age_category'),
    path("age-category/delete/<int:pk>/", DeleteAgeCategoryView.as_view(), name='delete_age_category'),
] + router.urls
