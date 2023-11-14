from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .models import UserProfile



class MainPage(LoginRequiredMixin, ListView):
    context_object_name = 'main'
    template_name = 'vpn_app/main.html'
    model = UserProfile  # Предполагается, что UserProfile - это ваша модель

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logout_url'] = reverse_lazy('logout')  # URL для выхода пользователя
        return context
    context_object_name = 'main'
    template_name = 'vpn_app/main.html'



class RegisterPage(FormView):
    template_name = 'vpn_app/register.html'
    form_class = UserCreationForm  # Предположим, что вы используете стандартную форму создания пользователя
    redirect_authenticated_user = True
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super().get(*args, **kwargs)
    
class CustomLoginView(LoginView):
    template_name = 'vpn_app/login.html'  
    success_url = reverse_lazy('main')
    
class CustomLogoutView(LogoutView):
    next_page = 'login'  # Сюда можно поместить адрес, на который нужно перенаправить после выхода пользователя

