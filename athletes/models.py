from django.db import models
from django.db.models import Model


# Create your models here.

class GenderChoices(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'


class Athletes(models.Model):
    first_name = models.CharField(
        max_length=50
    )
    last_name = models.CharField(
        max_length=50
    )
    nationality = models.CharField(
        max_length=50
    )
    birth_date = models.DateField(
        null=False,
        blank=False
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices
    )
    disciplines = models.ManyToManyField( # many to many relation with discipline table
        'Disciplines',
        related_name='athletes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class AgeCategories(models.Model):
    class Name(models.TextChoices):
        UNDER_14 = 'U14', 'Under 14'
        UNDER_16 = 'U16', 'Under 16'
        UNDER_18 = 'U18', 'Under 18'
        UNDER_20 = 'U20', 'Under 20'
        UNDER_23 = 'U23', 'Under 23'
        SENIOR_OPEN = 'SEN', 'Senior / Open'
        VETERANS_35 = 'V35', 'Veterans 35–39'
        VETERANS_40 = 'V40', 'Veterans 40–44'
        VETERANS_45 = 'V45', 'Veterans 45–49'
        VETERANS_50 = 'V50', 'Veterans 50–54'
        VETERANS_55 = 'V55', 'Veterans 55–59'
        VETERANS_60 = 'V60', 'Veterans 60+'

    name = models.CharField(
        max_length=4,
        choices=Name.choices
    )

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices
    )

    min_age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    max_age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [  # we can have each age category name appear only twice - for M and F gender. (for e.g. U20 M and U20 F)
            models.UniqueConstraint(fields=['name', 'gender'], name='unique_name_gender')
        ]

    def save(self, *args, **kwargs):
        category_age_map = {
            'U14': (12, 14),
            'U16': (14, 16),
            'U18': (16, 18),
            'U20': (18, 20),
            'U23': (20, 23),
            'SEN': (20, None),  # no upper limit for senior
            'V35': (35, 39),
            'V40': (40, 44),
            'V45': (45, 49),
            'V50': (50, 54),
            'V55': (55, 59),
            'V60': (60, None),  # no upper limit
        }

        if self.name in category_age_map:
            self.min_age, self.max_age = category_age_map[
                self.name]  # unpack the tuple and set min and max age based on category name

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.get_name_display()} ({self.get_gender_display()})"


class Disciplines(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=True
    )

    def __str__(self) -> str:
        return self.name
