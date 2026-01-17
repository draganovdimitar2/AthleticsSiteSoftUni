from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from athletes.models import Disciplines


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'common/home.html')


def redirect_home(request: HttpRequest) -> HttpResponse:
    return redirect('common:home_page')


def disciplines(request: HttpRequest) -> HttpResponse:
    all_disciplines = Disciplines.objects.all()
    context = {
        "disciplines": all_disciplines
    }
    return render(request, 'common/disciplines.html', context)
