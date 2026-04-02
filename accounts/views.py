from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class RegisterUserView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'


class LogoutUserView(LogoutView):
    pass
