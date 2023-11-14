from django.urls import path
from .views import RegisterPage, MainPage, CustomLogoutView, CustomLoginView

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('main/', MainPage.as_view(), name='main'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(next_page='main'), name='login'),
    # Другие URL-маршруты вашего приложения
] 