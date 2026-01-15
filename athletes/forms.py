from django import forms
from datetime import date
from .models import Athletes


class CreateAthlete(forms.ModelForm):

    class Meta:
        model = Athletes
        fields = [
            'first_name',
            'last_name',
            'nationality',
            'birth_date',
            'gender',
        ]

        # ✔ Custom labels
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'birth_date': 'Date of Birth',
        }

        # ✔ Help texts
        help_texts = {
            'birth_date': 'Use the format YYYY-MM-DD.',
            'nationality': 'Enter the country of citizenship.',
        }

        # ✔ Placeholders + widgets
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ivan'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ivanov'
            }),
            'nationality': forms.TextInput(attrs={
                'placeholder': 'Bulgarian'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

        # ✔ Custom error messages
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

    # birth date validation
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            age = date.today().year - birth_date.year
            if age < 10:
                raise forms.ValidationError(
                    'Athlete must be at least 10 years old.'
                )
        return birth_date
