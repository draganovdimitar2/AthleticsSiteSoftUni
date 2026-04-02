from django.urls import path
from common.views import HomePageView, RedirectHomeView, DisciplinesView, ContactPageView, AgeCategoriesView, CompetitionCategoriesView

app_name = 'common'
urlpatterns = [
    path("", HomePageView.as_view(), name='home_page'),
    path('redirect-home/', RedirectHomeView.as_view(), name='redirect_home'),
    path("disciplines/", DisciplinesView.as_view(), name='disciplines'),
    path("age-categories/", AgeCategoriesView.as_view(), name='age_categories'),
    path("competition-categories/", CompetitionCategoriesView.as_view(), name='competition_categories'),
    path("contact/", ContactPageView.as_view(), name='contact_page'),
]
