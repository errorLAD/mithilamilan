from django.urls import path
from . import views

app_name = 'ghatkaiti'

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('create/', views.profile_create, name='profile_create'),
    path('profile/<slug:slug>/', views.profile_detail, name='profile_detail'),
]
