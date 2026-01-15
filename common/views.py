from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'common/home.html')

def redirect_home(request: HttpRequest) -> HttpResponse:
    return redirect('common:home_page')