from django.urls import path
from common.views import home_page, redirect_home, disciplines, contact_page, age_categories, competition_categories

app_name = 'common'
urlpatterns = [
    path("", home_page, name='home_page'),
    path('redirect-home/', redirect_home, name='redirect_home'),
    path("disciplines/", disciplines, name='disciplines'),
    path("age-categories/", age_categories, name='age_categories'),
    path("competition-categories/", competition_categories, name='competition_categories'),
    path("contact/", contact_page, name='contact_page'),
]
