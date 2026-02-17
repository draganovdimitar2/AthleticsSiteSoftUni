from django.urls import path
from common.views import home_page, redirect_home, disciplines, contact_page, test_404_view

app_name = 'common'
urlpatterns = [
    path("", home_page, name='home_page'),
    path('redirect-home/', redirect_home, name='redirect_home'),
    path("disciplines/", disciplines, name='disciplines'),
    path("contact/", contact_page, name='contact_page'),
    path("test-404/", test_404_view, name='test_404'),  # custom error 404 page
]
