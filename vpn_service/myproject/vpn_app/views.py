from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.db.models import Sum
from django.shortcuts import get_object_or_404
import requests
from django.views import View
from django.db.models import Sum

from .models import UserProfile, UserSite, UserSiteTraffic
from .forms import UserChangeForm



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
    success_url = reverse_lazy('cabinet')

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
        form.instance.user_profile = self.request.user.userprofile 
        return super().form_valid(form)

class SitesList(ListView):
    model = UserSite
    context_object_name = 'user_sites'  
    template_name = 'vpn_app/user_profiles_list.html'  

    def get_queryset(self):
        return UserSite.objects.filter(user_profile=self.request.user.userprofile)
 


class SiteDetailsView(View):
    def get(self, request, site_id):
        site = get_object_or_404(UserSite, pk=site_id)

        user_site_traffic_instance, created = UserSiteTraffic.objects.get_or_create(user_site=site)

        user_site_traffic_instance.increment_clicks()

        proxies = {
            "http": "http://scraperapi:35885be67a5cac5e0747eb5d2bb172bf@proxy-server.scraperapi.com:8001"
        }

        try:
            r = requests.get(site.site_url, proxies=proxies, verify=False)
            data = r.text  
        except requests.RequestException as e:
            data = f"Error: {e}"  

        

        return render(request, 'vpn_app/site_details.html', {'data': data})
    
class UserCabinetView(View):
    template_name = 'vpn_app/cabinet.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)

            context['user_first_name'] = user_profile.first_name
            context['user_last_name'] = user_profile.last_name

            total_clicks = UserSiteTraffic.objects.filter(user_site__user_profile=user_profile).aggregate(Sum('clicks'))['clicks__sum']
            context['total_clicks'] = total_clicks if total_clicks is not None else 0  

            

        return render(request, self.template_name, context)
    


