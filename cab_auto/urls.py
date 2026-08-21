from django.urls import path
from . import views

app_name = 'cab_auto'

urlpatterns = [
    path('', views.cab_auto_home, name='cab_auto_home'),
    path('directory/', views.driver_list, name='driver_list'),
    path('auto/', views.driver_list, {'forced_type': 'auto'}, name='auto_list'),
    path('taxi/', views.driver_list, {'forced_type': 'taxi'}, name='taxi_list'),
    path('register/', views.driver_register, name='driver_register'),
    path('driver/<slug:slug>/', views.driver_detail, name='driver_detail'),
]
