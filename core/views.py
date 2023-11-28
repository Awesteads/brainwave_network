from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from item.models import Category, Item
from django.db.models import Count
from post.models import Post
from .forms import SignupForm, LoginForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def brainwave(request):
    # Obtenha os posts ordenados pela contagem de curtidas (do maior para o menor)
    posts_by_likes = Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')

    # Obtenha os posts ordenados pela data de criação (do mais recente para o mais antigo)
    posts_by_date = Post.objects.all().order_by('-created_at')

    # Renderize o template 'brainwave.html' com as duas listas de posts
    return render(request, 'core/brainwave.html', {'posts_by_likes': posts_by_likes, 'posts_by_date': posts_by_date})

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
    
@login_required
def delete_account(request):
    # Excluir o usuário e desconectar
    request.user.delete()
    logout(request)
    return redirect('core:brainwave')  