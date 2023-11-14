from django.shortcuts import render
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Дополнительные действия после успешной регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'vpn_app/register.html', {'form': form})