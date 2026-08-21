from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('submit/', views.event_submit, name='event_submit'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('<slug:slug>/ics/', views.event_ics_export, name='event_ics'),
]
