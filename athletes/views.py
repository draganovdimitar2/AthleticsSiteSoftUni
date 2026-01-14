from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from athletes.models import Athletes


# Create your views here.
def list_athletes(request: HttpRequest) -> HttpResponse:
    athletes = Athletes.objects.all()
    context = {
        'athletes': athletes
    }
    return render(request, 'athletes/list_athletes.html', context)
