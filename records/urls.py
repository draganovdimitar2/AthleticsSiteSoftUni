from django.urls import path
from records.views import results

urlpatterns = [
    path("results/", results, name='results')
]
