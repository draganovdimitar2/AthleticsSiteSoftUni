from django.db import models


# Create your models here.
class Athletes(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

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
        choices=Gender.choices
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
