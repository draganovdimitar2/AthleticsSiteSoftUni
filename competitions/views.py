from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from competitions.models import Competition


# Create your views here.
def list_competitions(request: HttpRequest) -> HttpResponse:
    all_competitions = Competition.objects.all().order_by('-end_date')
    context = {
        "competitions": all_competitions
    }
    return render(request, 'competitions/list_competitions.html', context)
