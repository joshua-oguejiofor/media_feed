from django.urls import path
from . import views 


urlpatterns = [
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment')
]