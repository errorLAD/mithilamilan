from django.urls import path
from . import views, views_moderation

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('set-location/', views.set_location, name='set_location'),
    path('about/', views.about, name='about'),
    
    # Clean Legal Page URLs
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('cancellation/', views.cancellation, name='cancellation'),
    path('community-guidelines/', views.community_guidelines, name='community_guidelines'),
    path('content-policy/', views.content_policy, name='content_policy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    
    # Support & Contact
    path('contact/', views.contact, name='contact'),
    path('support/', views.contact, name='support'),
    path('report-issue/', views.report_issue, name='report_issue'),
    
    # Moderation & Submission Tracking
    path('moderation/', views_moderation.moderation_dashboard, name='moderation_dashboard'),
    path('moderation/<str:item_type>/<int:pk>/<str:action>/', views_moderation.moderation_action, name='moderation_action'),
    path('my-submissions/', views_moderation.user_submissions, name='user_submissions'),
]