from django.views.generic import TemplateView, ListView, RedirectView
from athletes.models import Discipline, AgeCategory, Athlete
from competitions.models import CompetitionCategory, Competition
from records.models import Results


class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['athletes_count'] = Athlete.objects.count()
        context['competitions_count'] = Competition.objects.count()
        context['results_count'] = Results.objects.count()
        context['latest_results'] = Results.objects.order_by('-result_date')[:3]
        return context


class RedirectHomeView(RedirectView):
    pattern_name = 'common:home_page'


class DisciplinesView(ListView):
    model = Discipline
    template_name = 'common/disciplines.html'
    context_object_name = 'disciplines'


class AgeCategoriesView(ListView):
    model = AgeCategory
    template_name = 'common/age_categories.html'
    context_object_name = 'age_categories'


class CompetitionCategoriesView(ListView):
    model = CompetitionCategory
    template_name = 'common/competition_categories.html'
    context_object_name = 'competition_categories'


class ContactPageView(TemplateView):
    template_name = 'common/contact.html'


class Custom404View(TemplateView):
    template_name = 'common/404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response
