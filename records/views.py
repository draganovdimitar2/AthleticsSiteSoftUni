from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q
from athletes.models import Athlete, AgeCategory
from athletes.utils import calculate_age
from competitions.models import Competition
from .models import Results
from .forms import ResultsForm

# Create your views here.
def get_age_category_ajax(request: HttpRequest) -> JsonResponse:
    athlete_id = request.GET.get('athlete_id')
    competition_id = request.GET.get('competition_id')

    if not competition_id:
        return JsonResponse({'error': 'Missing competition_id'}, status=400)

    try:
        competition = Competition.objects.get(pk=competition_id)
        categories = competition.age_groups.all()
        
        selected_id = None
        if athlete_id:
            try:
                athlete = Athlete.objects.get(pk=athlete_id)
                athlete_age = calculate_age(athlete.birth_date, competition.start_date)

                match = competition.age_groups.filter(
                    gender=athlete.gender
                ).filter(
                    Q(min_age__lte=athlete_age) | Q(min_age__isnull=True),
                    Q(max_age__gte=athlete_age) | Q(max_age__isnull=True)
                ).first()

                if match:
                    selected_id = match.id
            except (Athlete.DoesNotExist, ValueError):
                pass

        return JsonResponse({
            'categories': [{'id': c.id, 'name': str(c)} for c in categories],
            'selected_id': selected_id
        })

    except Competition.DoesNotExist:
        return JsonResponse({'error': 'Competition not found'}, status=404)


def results(request: HttpRequest) -> HttpResponse:
    all_results = Results.objects.all()

    selected_year = request.GET.get('year')
    selected_competition_name = request.GET.get('competition_name')

    if selected_year:
        all_results = all_results.filter(result_date__year=selected_year)
    
    if selected_competition_name:
        all_results = all_results.filter(competition__name__icontains=selected_competition_name)

    for r in all_results:
        r.unit = 's' if r.discipline.name[0].isdigit() else 'm'

    context = {
        'results': all_results,
        'years': sorted({r.result_date.year for r in Results.objects.all()}),
        'selected_year': int(selected_year) if selected_year else None,
        'selected_competition_name': selected_competition_name,
        'competitions': {r.competition for r in Results.objects.all()}
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('records/_results_partial.html', context, request=request)
        return HttpResponse(html)
    else:
        return render(request, 'records/list.html', context)


def create_result(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ResultsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('results')
    else:
        form = ResultsForm()
    context = {
        'form': form
    }
    return render(request, 'records/create_result.html', context)


def update_result(request: HttpRequest, pk: int) -> HttpResponse:
    result = get_object_or_404(Results, pk=pk)
    if request.method == "POST":
        form = ResultsForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect('results')
    else:
        form = ResultsForm(instance=result)
    context = {
        'form': form,
        'result': result
    }
    return render(request, 'records/update_result.html', context)


def delete_result(request: HttpRequest, pk: int) -> HttpResponse:
    result = get_object_or_404(Results, pk=pk)
    if request.method == "POST":
        result.delete()
        return redirect('results')
    else:
        context = {
            'result': result
        }
        return render(request, 'records/confirm_result_deletion.html', context)
