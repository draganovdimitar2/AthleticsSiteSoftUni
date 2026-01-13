from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def list_athletes(request: HttpRequest) -> HttpResponse:
    return render(request, 'athletes/list_athletes.html')