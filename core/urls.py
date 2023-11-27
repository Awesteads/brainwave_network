from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import logout_view
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('register/', views.signup, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout_view, name='logout'),

    path('brainwave/', views.brainwave, name='brainwave'),
]