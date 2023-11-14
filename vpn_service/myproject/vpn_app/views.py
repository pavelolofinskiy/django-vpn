from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
import requests
from django.http import HttpResponse
from django.views import View

from .models import UserProfile, UserSite
from .forms import UserChangeForm, UserProfileForm


from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import UserProfile

class MainPage(ListView):
    context_object_name = 'main'
   
    template_name = 'vpn_app/main.html'
    model = UserProfile
    
    def get_queryset(self):
        return UserProfile.objects.all()
    
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


class ProxyView(View):
    def get(self, request, site_name, url):
        api_key = '35885be67a5cac5e0747eb5d2bb172bf'  # Replace with your actual API key
        scraperapi_url = f"http://api.scraperapi.com?api_key={api_key}&url=https://{url}"

        try:
            response = requests.get(scraperapi_url)  # Make a request to the Scraper API

            if response.status_code == 200:
                modified_content = self.modify_content(response.content, site_name)
                return HttpResponse(modified_content, content_type=response.headers['content-type'])

        except requests.RequestException as e:
            return HttpResponse(f'Failed to fetch the requested URL: {e}', status=500)

    def modify_content(self, content, site_name):
        modified_content = content.replace(b'https://external-site.com', f'/proxy/{site_name}/external-site.com'.encode())
        return modified_content

class SiteCreateView(LoginRequiredMixin, CreateView):
    model = UserSite 
    fields = '__all__'
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
    
class ProfileData(FormView):
    form_class = UserProfileForm  
    context_object_name = 'profile_data'
    template_name = 'vpn_app/profile_data.html'
    

