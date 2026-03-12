from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from athletes.models import Athlete, Discipline, AgeCategory
from .forms import CreateAthlete, UpdateAthlete, DisciplineForm, AgeCategoryForm


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
        form = UpdateAthlete(request.POST, instance=athlete)
        if form.is_valid():
            form.save()
            return redirect('athletes:list')
    else:  # load the form if request is "GET"
        form = UpdateAthlete(instance=athlete)
    context = {
        'form': form
    }
    return render(request, 'athletes/update_athlete.html', context)


def confirm_delete_athlete(request: HttpRequest, athlete_id: int) -> HttpResponse:
    athlete_to_delete = get_object_or_404(Athlete, pk=athlete_id)
    if request.method == "POST":
        athlete_to_delete.delete()
        return redirect('athletes:list')
    else:
        context = {
            'athlete_to_delete': athlete_to_delete
        }
        return render(request, 'athletes/confirm_athlete_deletion.html', context)


def create_discipline(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DisciplineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common:disciplines')
    else:
        form = DisciplineForm()
    context = {
        'form': form
    }
    return render(request, 'athletes/create_discipline.html', context)


def update_discipline(request: HttpRequest, pk: int) -> HttpResponse:
    discipline = get_object_or_404(Discipline, pk=pk)
    if request.method == "POST":
        form = DisciplineForm(request.POST, instance=discipline)
        if form.is_valid():
            form.save()
            return redirect('common:disciplines')
    else:
        form = DisciplineForm(instance=discipline)
    context = {
        'form': form,
        'discipline': discipline
    }
    return render(request, 'athletes/update_discipline.html', context)


def delete_discipline(request: HttpRequest, pk: int) -> HttpResponse:
    discipline = get_object_or_404(Discipline, pk=pk)
    if request.method == "POST":
        discipline.delete()
        return redirect('common:disciplines')
    else:
        context = {
            'discipline': discipline
        }
        return render(request, 'athletes/confirm_discipline_deletion.html', context)


def create_age_category(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AgeCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common:age_categories')
    else:
        form = AgeCategoryForm()
    context = {
        'form': form
    }
    return render(request, 'athletes/create_age_category.html', context)


def update_age_category(request: HttpRequest, pk: int) -> HttpResponse:
    age_category = get_object_or_404(AgeCategory, pk=pk)
    if request.method == "POST":
        form = AgeCategoryForm(request.POST, instance=age_category)
        if form.is_valid():
            form.save()
            return redirect('common:age_categories')
    else:
        form = AgeCategoryForm(instance=age_category)
    context = {
        'form': form,
        'age_category': age_category
    }
    return render(request, 'athletes/update_age_category.html', context)


def delete_age_category(request: HttpRequest, pk: int) -> HttpResponse:
    age_category = get_object_or_404(AgeCategory, pk=pk)
    if request.method == "POST":
        age_category.delete()
        return redirect('common:age_categories')
    else:
        context = {
            'age_category': age_category
        }
        return render(request, 'athletes/confirm_age_category_deletion.html', context)
