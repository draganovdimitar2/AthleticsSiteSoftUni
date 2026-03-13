from django import forms
from .models import Results


class ResultsForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = [
            'athlete',
            'competition',
            'discipline',
            'age_category',
            'position',
            'result_value',
            'result_date'
        ]
        widgets = {
            'result_date': forms.DateInput(attrs={'type': 'date'}),
            'age_category': forms.Select(attrs={'disabled': 'disabled'}),
        }
