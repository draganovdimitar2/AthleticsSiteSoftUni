from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from athletes.models import Athlete, Discipline, AgeCategory
from .forms import CreateAthlete, UpdateAthlete, DisciplineForm, AgeCategoryForm


from rest_framework import viewsets, permissions
from .serializers import AthleteSerializer

class AthleteViewSet(viewsets.ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OverviewView(TemplateView):
    template_name = 'athletes/overview.html'


class ListAthletesView(ListView):
    model = Athlete
    template_name = 'athletes/list_athletes.html'
    context_object_name = 'athletes'


class CreateAthleteView(LoginRequiredMixin, CreateView):
    model = Athlete
    form_class = CreateAthlete
    template_name = 'athletes/create_athlete.html'
    success_url = reverse_lazy('athletes:list')


class UpdateAthleteView(LoginRequiredMixin, UpdateView):
    model = Athlete
    form_class = UpdateAthlete
    template_name = 'athletes/update_athlete.html'
    pk_url_kwarg = 'athlete_id'
    success_url = reverse_lazy('athletes:list')


class DeleteAthleteView(LoginRequiredMixin, DeleteView):
    model = Athlete
    template_name = 'athletes/confirm_athlete_deletion.html'
    pk_url_kwarg = 'athlete_id'
    context_object_name = 'athlete_to_delete'
    success_url = reverse_lazy('athletes:list')


class CreateDisciplineView(LoginRequiredMixin, CreateView):
    model = Discipline
    form_class = DisciplineForm
    template_name = 'athletes/create_discipline.html'
    success_url = reverse_lazy('common:disciplines')


class UpdateDisciplineView(LoginRequiredMixin, UpdateView):
    model = Discipline
    form_class = DisciplineForm
    template_name = 'athletes/update_discipline.html'
    success_url = reverse_lazy('common:disciplines')


class DeleteDisciplineView(LoginRequiredMixin, DeleteView):
    model = Discipline
    template_name = 'athletes/confirm_discipline_deletion.html'
    context_object_name = 'discipline'
    success_url = reverse_lazy('common:disciplines')


class CreateAgeCategoryView(LoginRequiredMixin, CreateView):
    model = AgeCategory
    form_class = AgeCategoryForm
    template_name = 'athletes/create_age_category.html'
    success_url = reverse_lazy('common:age_categories')


class UpdateAgeCategoryView(LoginRequiredMixin, UpdateView):
    model = AgeCategory
    form_class = AgeCategoryForm
    template_name = 'athletes/update_age_category.html'
    success_url = reverse_lazy('common:age_categories')


class DeleteAgeCategoryView(LoginRequiredMixin, DeleteView):
    model = AgeCategory
    template_name = 'athletes/confirm_age_category_deletion.html'
    context_object_name = 'age_category'
    success_url = reverse_lazy('common:age_categories')
