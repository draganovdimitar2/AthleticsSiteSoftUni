from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .models import Results
from .forms import ResultsForm

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
