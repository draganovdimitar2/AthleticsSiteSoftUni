from django.db import models
from django.db.models import ForeignKey, Q
from django.core.exceptions import ValidationError
from athletes.utils import calculate_age

# ... (rest of models.py imports and class Results definition)


# Create your models here.
class Results(models.Model):
    athlete = models.ForeignKey(
        'athletes.Athlete',
        on_delete=models.CASCADE,
        related_name='results'
    )
    competition = models.ForeignKey(
        'competitions.Competition',
        on_delete=models.CASCADE,
        related_name='results'
    )
    discipline = models.ForeignKey(
        'athletes.Discipline',
        on_delete=models.CASCADE,
        related_name='results'
    )
    age_category = models.ForeignKey(  # age category must match athletes birth_date otherwise we will have data inconsistency
        'athletes.AgeCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='results'
    )
    position = models.PositiveIntegerField()

    result_value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        help_text='Time (seconds) or distance (meters)'
    )
    result_date = models.DateField()  # result date must be between start_date and end_date of competitions table, otherwise data is inconsistent

    def _get_matching_age_category(self):
        if not (self.athlete and self.competition):
            return None
        
        competition_date = self.competition.start_date
        athlete_age = calculate_age(
            self.athlete.birth_date,
            competition_date
        )

        return self.competition.age_groups.filter(
            gender=self.athlete.gender
        ).filter(
            Q(min_age__lte=athlete_age) | Q(min_age__isnull=True),
            Q(max_age__gte=athlete_age) | Q(max_age__isnull=True)
        ).first()

    def clean(self):
        errors = {}

        # validate result_date vs competition dates
        if self.competition and self.result_date:
            if not (
                    self.competition.start_date
                    <= self.result_date
                    <= self.competition.end_date
            ):
                errors['result_date'] = (
                    'Result date must be within the competition dates '
                    f'({self.competition.start_date} – {self.competition.end_date}).'
                )

        # auto-assign age category if missing
        if self.athlete and self.competition and not self.age_category:
            self.age_category = self._get_matching_age_category()
            if not self.age_category:
                errors['age_category'] = 'No matching age category found for this athlete in this competition.'

        # validate age category consistency
        if self.athlete and self.age_category and self.competition:
            competition_date = self.competition.start_date
            athlete_age = calculate_age(
                self.athlete.birth_date,
                competition_date
            )

            if self.age_category.min_age is not None:
                if athlete_age < self.age_category.min_age:
                    errors['age_category'] = (
                        f'Athlete is {athlete_age} years old and does not fit '
                        f'{self.age_category.get_name_display()}.'
                    )

            if self.age_category.max_age is not None:
                if athlete_age > self.age_category.max_age:
                    errors['age_category'] = (
                        f'Athlete is {athlete_age} years old and does not fit '
                        f'{self.age_category.get_name_display()}.'
                    )

            # validate gender match
            if self.athlete.gender != self.age_category.gender:
                errors['age_category'] = (
                    'Athlete gender does not match age category gender.'
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()  # to validate everything before saving the model
        super().save(*args, **kwargs)
