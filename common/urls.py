from django.urls import path
from common.views import home_page, redirect_home, disciplines

app_name = 'common'
urlpatterns = [
    path("", home_page, name='home_page'),
    path('redirect-home/', redirect_home, name='redirect_home'),
    path("disciplines/", disciplines, name='disciplines')
]
