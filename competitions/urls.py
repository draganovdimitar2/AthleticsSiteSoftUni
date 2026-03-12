from django.urls import path
from .views import list_competitions, create_competition, update_competition, delete_competition, \
    create_competition_category, update_competition_category, delete_competition_category

app_name = 'competitions'

urlpatterns = [
    path('list/', list_competitions, name='list'),
    path('create/', create_competition, name='create'),
    path('update/<int:pk>/', update_competition, name='update'),
    path('delete/<int:pk>/', delete_competition, name='delete'),
    path('category/create/', create_competition_category, name='create_competition_category'),
    path('category/update/<int:pk>/', update_competition_category, name='update_competition_category'),
    path('category/delete/<int:pk>/', delete_competition_category, name='delete_competition_category'),
]
