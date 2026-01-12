from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'common/home.html')