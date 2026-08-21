from django.urls import path
from . import views

app_name = 'subreddits'

urlpatterns = [
    path('', views.subreddit_list, name='list'),
    path('create/', views.subreddit_create, name='create'),
    path('r/<slug:slug>/', views.subreddit_detail, name='subreddit_detail'),
    path('r/<slug:slug>/edit/', views.subreddit_edit, name='edit'),
    path('r/<slug:slug>/subscribe/', views.subscribe, name='subscribe'),
    path('r/<slug:slug>/unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('approval/', views.subreddit_approval_list, name='approval_list'),
    path('r/<slug:slug>/approve/', views.approve_subreddit, name='approve'),
    path('r/<slug:slug>/reject/', views.reject_subreddit, name='reject'),
    path('search/', views.search, name='search'),
] 