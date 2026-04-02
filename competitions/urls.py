from django.urls import path
from .views import ListCompetitionsView, CreateCompetitionView, UpdateCompetitionView, DeleteCompetitionView, \
    CreateCompetitionCategoryView, UpdateCompetitionCategoryView, DeleteCompetitionCategoryView

app_name = 'competitions'

urlpatterns = [
    path('list/', ListCompetitionsView.as_view(), name='list'),
    path('create/', CreateCompetitionView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateCompetitionView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteCompetitionView.as_view(), name='delete'),
    path('category/create/', CreateCompetitionCategoryView.as_view(), name='create_competition_category'),
    path('category/update/<int:pk>/', UpdateCompetitionCategoryView.as_view(), name='update_competition_category'),
    path('category/delete/<int:pk>/', DeleteCompetitionCategoryView.as_view(), name='delete_competition_category'),
]
