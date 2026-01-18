from django import forms
from datetime import date
from .models import Athlete


class CreateAthlete(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  # only set default birthdate when obj is new
            self.fields['birth_date'].initial = date(2000, 1, 1)  # force the calendar to start at 01/01/2000

    class Meta:
        model = Athlete
        fields = [
            'first_name',
            'last_name',
            'nationality',
            'birth_date',
            'gender',
            'disciplines'
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'birth_date': 'Date of Birth',
        }

        help_texts = {
            'birth_date': 'Use the format YYYY-MM-DD.',
            'nationality': 'Enter the country of citizenship.',
            'disciplines': 'Hold down “Control”, or “Command” on a Mac, to select more than one.'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ivan'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ivanov'}),
            'nationality': forms.TextInput(attrs={'placeholder': 'Bulgarian'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

        error_messages = {
            'first_name': {
                'required': 'First name is required.',
                'max_length': 'First name cannot exceed 50 characters.',
            },
            'last_name': {
                'required': 'Last name is required.',
            },
            'birth_date': {
                'required': 'Please enter a valid birth date.',
            },
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            age = date.today().year - birth_date.year
            if age < 10:
                raise forms.ValidationError('Athlete must be at least 10 years old.')
        return birth_date
