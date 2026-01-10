from django.urls import path
from results.views import results

urlpatterns = [
    path("/results", results, name='results')
]
