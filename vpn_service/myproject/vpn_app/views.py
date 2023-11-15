from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .forms import UserChangeForm
import requests

from .models import UserProfile, UserSite



class MainPage(LoginRequiredMixin, ListView):
    context_object_name = 'main'
    template_name = 'vpn_app/main.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            context['user_first_name'] = user_profile.first_name
            context['user_last_name'] = user_profile.last_name
            context['logout_url'] = reverse_lazy('logout')
        return context



class RegisterPage(FormView):
    template_name = 'vpn_app/register.html'
    form_class = UserCreationForm  
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
    next_page = 'login' 


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'vpn_app/edit_profile.html'
    form_class = UserChangeForm 
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user_profile = form.save(commit=False)
        user_profile.user = self.request.user
        user_profile.save()
        return super().form_valid(form)
    
    def get_object(self):
        return self.request.user.userprofile  


class SiteCreateView(LoginRequiredMixin, CreateView):
    model = UserSite 
    fields = ['site_name', 'site_url']
    success_url = reverse_lazy('main')  
    template_name = 'vpn_app/site_create.html'

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.userprofile  # Assuming 'userprofile' is the related name
        return super().form_valid(form)

class SitesList(ListView):
    model = UserSite
    context_object_name = 'user_sites'  # Renaming 'sites' to 'user_profiles' for clarity
    template_name = 'vpn_app/user_profiles_list.html'  # You should specify the appropriate template

    def get_queryset(self):
        return UserSite.objects.all()
 


class SiteDetailsView(View):
    def get(self, request, site_id):
        site = get_object_or_404(UserSite, pk=site_id)
        proxies = {
            "http": "http://scraperapi:35885be67a5cac5e0747eb5d2bb172bf@proxy-server.scraperapi.com:8001"
        }

        try:
            # Making a request through the proxy
            r = requests.get(site.site_url, proxies=proxies, verify=False)
            data = r.text  # Получение данных от прокси
        except requests.RequestException as e:
            data = f"Error: {e}"  # Обработка ошибки, если запрос через прокси не выполнен

        return render(request, 'vpn_app/site_details.html', {'data': data})