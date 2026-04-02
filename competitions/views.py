from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from competitions.models import Competition, CompetitionCategory
from .forms import CompetitionForm, CompetitionCategoryForm


class ListCompetitionsView(ListView):
    model = Competition
    template_name = 'competitions/list_competitions.html'
    context_object_name = 'competitions'
    ordering = ['-end_date']


class CreateCompetitionView(LoginRequiredMixin, CreateView):
    model = Competition
    form_class = CompetitionForm
    template_name = 'competitions/create_competition.html'
    success_url = reverse_lazy('competitions:list')


class UpdateCompetitionView(LoginRequiredMixin, UpdateView):
    model = Competition
    form_class = CompetitionForm
    template_name = 'competitions/update_competition.html'
    success_url = reverse_lazy('competitions:list')


class DeleteCompetitionView(LoginRequiredMixin, DeleteView):
    model = Competition
    template_name = 'competitions/confirm_competition_deletion.html'
    context_object_name = 'competition'
    success_url = reverse_lazy('competitions:list')


class CreateCompetitionCategoryView(LoginRequiredMixin, CreateView):
    model = CompetitionCategory
    form_class = CompetitionCategoryForm
    template_name = 'competitions/create_competition_category.html'
    success_url = reverse_lazy('common:competition_categories')


class UpdateCompetitionCategoryView(LoginRequiredMixin, UpdateView):
    model = CompetitionCategory
    form_class = CompetitionCategoryForm
    template_name = 'competitions/update_competition_category.html'
    context_object_name = 'category'
    success_url = reverse_lazy('common:competition_categories')


class DeleteCompetitionCategoryView(LoginRequiredMixin, DeleteView):
    model = CompetitionCategory
    template_name = 'competitions/confirm_competition_category_deletion.html'
    context_object_name = 'category'
    success_url = reverse_lazy('common:competition_categories')
