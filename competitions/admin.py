from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CompetitionCategory, Competition


# Register your models here.

@admin.register(CompetitionCategory)
class CompetitionCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', ]
    search_fields = ['category_name', ]
    list_filter = ['category_name', ]


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city']
    search_fields = ['name', 'country']
    list_filter = ['name', 'country']
