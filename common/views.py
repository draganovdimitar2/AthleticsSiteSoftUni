from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from athletes.models import Discipline, AgeCategory, Athlete
from competitions.models import CompetitionCategory, Competition
from records.models import Results


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    athletes_count = Athlete.objects.count()
    competitions_count = Competition.objects.count()
    results_count = Results.objects.count()
    latest_results = Results.objects.order_by('-result_date')[:3]

    context = {
        'athletes_count': athletes_count,
        'competitions_count': competitions_count,
        'results_count': results_count,
        'latest_results': latest_results,
    }

    return render(request, 'common/home.html', context)


def redirect_home(request: HttpRequest) -> HttpResponse:
    return redirect('common:home_page')


def disciplines(request: HttpRequest) -> HttpResponse:
    all_disciplines = Discipline.objects.all()
    context = {
        "disciplines": all_disciplines
    }
    return render(request, 'common/disciplines.html', context)


def age_categories(request: HttpRequest) -> HttpResponse:
    all_age_categories = AgeCategory.objects.all()
    context = {
        "age_categories": all_age_categories
    }
    return render(request, 'common/age_categories.html', context)


def competition_categories(request: HttpRequest) -> HttpResponse:
    all_competition_categories = CompetitionCategory.objects.all()
    context = {
        "competition_categories": all_competition_categories
    }
    return render(request, 'common/competition_categories.html', context)


def contact_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'common/contact.html')


def custom_404_view(request, exception):
    return render(request, 'common/404.html', status=404)
