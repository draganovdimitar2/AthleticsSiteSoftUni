from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from competitions.models import Competition, CompetitionCategory
from .forms import CompetitionForm, CompetitionCategoryForm


# Create your views here.
def list_competitions(request: HttpRequest) -> HttpResponse:
    all_competitions = Competition.objects.all().order_by('-end_date')
    context = {
        "competitions": all_competitions
    }
    return render(request, 'competitions/list_competitions.html', context)


def create_competition(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('competitions:list')
    else:
        form = CompetitionForm()
    context = {
        'form': form
    }
    return render(request, 'competitions/create_competition.html', context)


def update_competition(request: HttpRequest, pk: int) -> HttpResponse:
    competition = get_object_or_404(Competition, pk=pk)
    if request.method == "POST":
        form = CompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            return redirect('competitions:list')
    else:
        form = CompetitionForm(instance=competition)
    context = {
        'form': form,
        'competition': competition
    }
    return render(request, 'competitions/update_competition.html', context)


def delete_competition(request: HttpRequest, pk: int) -> HttpResponse:
    competition = get_object_or_404(Competition, pk=pk)
    if request.method == "POST":
        competition.delete()
        return redirect('competitions:list')
    else:
        context = {
            'competition': competition
        }
        return render(request, 'competitions/confirm_competition_deletion.html', context)


def create_competition_category(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CompetitionCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common:competition_categories')
    else:
        form = CompetitionCategoryForm()
    context = {
        'form': form
    }
    return render(request, 'competitions/create_competition_category.html', context)


def update_competition_category(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(CompetitionCategory, pk=pk)
    if request.method == "POST":
        form = CompetitionCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('common:competition_categories')
    else:
        form = CompetitionCategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'competitions/update_competition_category.html', context)


def delete_competition_category(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(CompetitionCategory, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('common:competition_categories')
    else:
        context = {
            'category': category
        }
        return render(request, 'competitions/confirm_competition_category_deletion.html', context)
