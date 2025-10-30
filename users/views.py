from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import EmailAuthenticationForm, SignUpForm


class HomeView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')


class EmailLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'users/login.html'


class EmailLogoutView(LogoutView):
    next_page = reverse_lazy('home')
