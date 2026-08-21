from django.urls import path
from . import views

app_name = 'metro'

urlpatterns = [
    path('', views.metro_home, name='metro_home'),
] 