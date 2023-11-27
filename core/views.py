from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from item.models import Category, Item
from .forms import SignupForm, LoginForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html',{
        'categories': categories,
        'items': items,
    })

def brainwave(request):
    return render(request, 'core/brainwave.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('core:login')

    else:
        form = SignupForm()

    return render(request, 'core/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:brainwave')
    