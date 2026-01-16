from django.contrib import admin
from .models import Athletes, AgeCategories, Disciplines
# Register your models here.

@admin.register(Athletes)
class AthletesAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nationality', 'birth_date', 'gender']
    search_fields = ['first_name', 'last_name']
    list_filter = ['nationality', 'gender']

@admin.register(AgeCategories)
class AgeCategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'min_age', 'max_age']
    search_fields = ['name']
    list_filter = ['name', 'gender']

@admin.register(Disciplines)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
