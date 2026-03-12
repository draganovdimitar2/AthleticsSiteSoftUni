from django import forms
from .models import Competition, CompetitionCategory


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'name',
            'country',
            'city',
            'category',
            'start_date',
            'end_date',
            'age_groups'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CompetitionCategoryForm(forms.ModelForm):
    class Meta:
        model = CompetitionCategory
        fields = ['category_name']
