from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def results(request: HttpRequest) -> HttpResponse:
    return render(request, 'records/list.html')