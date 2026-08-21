from django.urls import path
from . import views, views_moderation

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('set-location/', views.set_location, name='set_location'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    
    # Moderation & Submission Tracking
    path('moderation/', views_moderation.moderation_dashboard, name='moderation_dashboard'),
    path('moderation/<str:item_type>/<int:pk>/<str:action>/', views_moderation.moderation_action, name='moderation_action'),
    path('my-submissions/', views_moderation.user_submissions, name='user_submissions'),
]