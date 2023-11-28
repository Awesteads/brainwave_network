from django.urls import path

from . import views
from .views import post_detail

app_name = 'post'

urlpatterns = [
    path('', views.posts, name='posts'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/', post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]