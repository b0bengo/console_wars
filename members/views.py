from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserOption

# Create your views here.

class RegistrationForm(UserCreationForm):
    OPTIONS = [
        ('nintendo_switch', 'Nintendo Switch'),
        ('xbox', 'Xbox'),
        ('pc', 'PC'),
        ('playstation', 'Playstation'),
    ]
    dropdown = forms.ChoiceField(choices=OPTIONS)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            option = form.cleaned_data.get('dropdown')
            UserOption.objects.create(user=user, option=option)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'members/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'members/login.html', {'error': 'Invalid credentials'})
    return render(request, 'members/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')