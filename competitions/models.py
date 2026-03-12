from django.db import models
from django.db.models import ForeignKey
from django.core.exceptions import ValidationError


# Create your models here.
class CompetitionCategory(models.Model):
    class Categories(models.TextChoices):
        INDOOR = "INDOOR", "Indoor"
        OUTDOOR = "OUTDOOR", "Outdoor"  # here can be added many more

    category_name = models.CharField(
        max_length=20,
        choices=Categories.choices,
        unique=True
    )

    def __str__(self) -> str:
        return self.category_name


class Competition(models.Model):
    name = models.CharField(
        max_length=150
    )
    country = models.CharField(
        max_length=50
    )
    city = models.CharField(
        max_length=50
    )
    age_groups = models.ManyToManyField(
        'athletes.AgeCategory',
        related_name='competitions'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    category = ForeignKey(
        CompetitionCategory,
        on_delete=models.PROTECT,
        related_name="competitions"
    )

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} is in country {self.country} and is {self.category}"
