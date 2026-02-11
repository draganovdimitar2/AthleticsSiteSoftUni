from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string # Added
from .models import Results

# Create your views here.
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
        'years': sorted({r.result_date.year for r in Results.objects.all()}), # Get all years from all results
        'selected_year': int(selected_year) if selected_year else None,
        'selected_competition_name': selected_competition_name,
        'competitions': {r.competition for r in Results.objects.all()} # Get all competitions from all results
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # If it's an AJAX request, return only the rendered partial HTML
        html = render_to_string('records/_results_partial.html', context, request=request)
        return HttpResponse(html)
    else:
        # For a regular request, render the full page
        return render(request, 'records/list.html', context)