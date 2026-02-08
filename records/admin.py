from django.contrib import admin
from .models import Results


# Register your models here.

@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ['athlete', 'age_category', 'competition', 'discipline', 'position', 'result_value', 'result_date']
    search_fields = ['athlete__first_name', 'athlete__last_name', 'competition__name']
    list_filter = ['age_category', 'discipline']
