from django.urls import path
from . import views

app_name = 'mithila_pride'

urlpatterns = [
    path('', views.person_list, name='person_list'),
    path('scholars/', views.person_list, {'forced_category': 'scholar'}, name='scholar_list'),
    path('submit/', views.person_submit, name='person_submit'),
    path('scholars/<slug:slug>/', views.person_detail, name='scholar_detail'),
    path('<slug:slug>/', views.person_detail, name='person_detail'),
]
