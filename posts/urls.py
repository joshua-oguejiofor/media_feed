from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('u/<str:username>/', views.profile_view, name='profile'),
    path('post/<int:pk>/update/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    
]
