from django.urls import path
from . import views

app_name = 'pandits'

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('pandits/', views.profile_list, {'forced_type': 'pandit'}, name='pandit_list'),
    path('astrologers/', views.profile_list, {'forced_type': 'astrologer'}, name='astrologer_list'),
    path('register/', views.profile_onboard, name='profile_onboard'),
    path('pandit/<slug:slug>/', views.profile_detail, name='pandit_detail'),
    path('astrologer/<slug:slug>/', views.profile_detail, name='astrologer_detail'),
    path('<slug:slug>/', views.profile_detail, name='profile_detail'),
]
