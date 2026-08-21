from django.urls import path
from . import views

app_name = 'mithila_panchang'

urlpatterns = [
    path('', views.panchang_home, name='panchang_home'),
    path('today/', views.today_panchang, name='today_panchang'),
    path('date/<str:date_str>/', views.date_detail, name='date_detail'),
    path('calendar/', views.monthly_calendar, name='monthly_calendar'),
    path('calendar/<int:year>/<int:month>/', views.monthly_calendar, name='monthly_calendar_specified'),
    path('months/', views.twelve_months, name='twelve_months'),
    path('festivals/', views.festivals_list, name='festivals_list'),
    path('festivals/<int:pk>/', views.festival_detail, name='festival_detail'),
    path('muhurat/', views.muhurat_hub, name='muhurat_hub'),
    path('muhurat/<slug:category_slug>/', views.muhurat_category_list, name='muhurat_category_list'),
    path('muhurat/date/<int:pk>/', views.muhurat_detail, name='muhurat_detail'),
    path('search/', views.panchang_search, name='panchang_search'),
    path('scanned-pages/', views.scanned_panchang, name='scanned_panchang'),
    path('download-ics/<str:event_type>/<int:item_id>/', views.download_ics, name='download_ics'),
    path('panchang-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('panchang-admin/verify/<int:pk>/', views.admin_verify_muhurat, name='admin_verify_muhurat'),
    path('songs/', views.mithila_songs_list, name='mithila_songs_list'),
]
