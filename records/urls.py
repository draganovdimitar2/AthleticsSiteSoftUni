from django.urls import path
from records.views import ResultsListView, CreateResultView, UpdateResultView, DeleteResultView, GetAgeCategoryAjaxView

urlpatterns = [
    path("", ResultsListView.as_view(), name='results'),
    path("create/", CreateResultView.as_view(), name='create_result'),
    path("update/<int:pk>/", UpdateResultView.as_view(), name='update_result'),
    path("delete/<int:pk>/", DeleteResultView.as_view(), name='delete_result'),
    path("get-age-category/", GetAgeCategoryAjaxView.as_view(), name='get_age_category_ajax'),
]
