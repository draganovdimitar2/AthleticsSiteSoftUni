from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from athletes.models import Athlete
from .forms import CreateAthlete
from django.shortcuts import get_object_or_404


# Create your views here.
def overview(request: HttpRequest) -> HttpResponse:
    return render(request, 'athletes/overview.html')


def list_athletes(request: HttpRequest) -> HttpResponse:
    athletes = Athlete.objects.all()
    context = {
        'athletes': athletes
    }
    return render(request, 'athletes/list_athletes.html', context)


def create_athlete(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateAthlete(request.POST)
        if form.is_valid():
            form.save()
            return redirect('athletes:list')
    else:  # load the form if request is "GET"
        form = CreateAthlete()
    context = {
        'form': form
    }
    return render(request, 'athletes/create_athlete.html', context)


def update_athlete(request: HttpRequest, athlete_id: int) -> HttpResponse:
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    if request.method == "POST":
        form = CreateAthlete(request.POST, instance=athlete)
        if form.is_valid():
            form.save()
            return redirect('athletes:list')
    else:  # load the form if request is "GET"
        form = CreateAthlete(instance=athlete)
    context = {
        'form': form
    }
    return render(request, 'athletes/update_athlete.html', context)


def delete_athlete(request: HttpRequest, athlete_id: int) -> HttpResponse:
    athlete_to_delete = get_object_or_404(Athlete, pk=athlete_id)
    athlete_to_delete.delete()
    return redirect('athletes:list')
