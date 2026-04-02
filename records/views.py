from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from athletes.models import Athlete
from athletes.utils import calculate_age
from competitions.models import Competition
from .models import Results
from .forms import ResultsForm


class GetAgeCategoryAjaxView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
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


class ResultsListView(ListView):
    model = Results
    template_name = 'records/list.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_year = self.request.GET.get('year')
        selected_competition_name = self.request.GET.get('competition_name')

        if selected_year:
            queryset = queryset.filter(result_date__year=selected_year)
        if selected_competition_name:
            queryset = queryset.filter(competition__name__icontains=selected_competition_name)
        
        for r in queryset:
            r.unit = 's' if r.discipline.name[0].isdigit() else 'm'
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_year = self.request.GET.get('year')
        selected_competition_name = self.request.GET.get('competition_name')

        context['years'] = sorted({r.result_date.year for r in Results.objects.all()})
        context['selected_year'] = int(selected_year) if selected_year else None
        context['selected_competition_name'] = selected_competition_name
        context['competitions'] = {r.competition for r in Results.objects.all()}
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('records/_results_partial.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class CreateResultView(LoginRequiredMixin, CreateView):
    model = Results
    form_class = ResultsForm
    template_name = 'records/create_result.html'
    success_url = reverse_lazy('results')


class UpdateResultView(LoginRequiredMixin, UpdateView):
    model = Results
    form_class = ResultsForm
    template_name = 'records/update_result.html'
    success_url = reverse_lazy('results')


class DeleteResultView(LoginRequiredMixin, DeleteView):
    model = Results
    template_name = 'records/confirm_result_deletion.html'
    context_object_name = 'result'
    success_url = reverse_lazy('results')
