from django.urls import path
from records.views import results, create_result, update_result, delete_result, get_age_category_ajax

urlpatterns = [
    path("", results, name='results'),
    path("create/", create_result, name='create_result'),
    path("update/<int:pk>/", update_result, name='update_result'),
    path("delete/<int:pk>/", delete_result, name='delete_result'),
    path("get-age-category/", get_age_category_ajax, name='get_age_category_ajax'),
]
