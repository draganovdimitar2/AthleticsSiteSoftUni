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
            'age_category': forms.Select(attrs={'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        athlete = cleaned_data.get('athlete')
        discipline = cleaned_data.get('discipline')

        if athlete and discipline:
            if not athlete.disciplines.filter(id=discipline.id).exists():
                self.add_error('discipline', f'Athlete {athlete} is not registered for discipline {discipline}.')
        
        return cleaned_data
