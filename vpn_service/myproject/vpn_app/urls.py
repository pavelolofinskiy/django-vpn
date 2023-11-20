from django.urls import path
from .views import RegisterPage, MainPage, CustomLogoutView, CustomLoginView, EditProfileView, SiteCreateView, SitesList, SiteDetailsView, UserCabinetView

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('main/', MainPage.as_view(), name='main'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(next_page='main'), name='login'),
    path('edit', EditProfileView.as_view(), name='edit'),
    path('site_create', SiteCreateView.as_view(), name='site_create'),
    path('user_sites', SitesList.as_view(), name='user_sites'),
    path('sites/<int:site_id>/', SiteDetailsView.as_view(), name='site_details'),
    path('cabinet/', UserCabinetView.as_view(), name='cabinet'),
    path('', CustomLogoutView.as_view(next_page='login'), name='logout'),
] 