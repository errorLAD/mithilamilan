from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mithila_panchang.views import mithila_songs_list
from core.admin_seo_views import sitemap_xml_view, robots_txt_view

urlpatterns = [
    path('sitemap.xml', sitemap_xml_view, name='sitemap_xml'),
    path('robots.txt', robots_txt_view, name='robots_txt'),
    path('admin/', admin.site.urls),
    path('admin-panel/', include('core.admin_urls', namespace='admin_panel')),
    path('', include('core.urls', namespace='core')),
    path('users/', include('users.urls')),
    path('', include('posts.urls')),
    path('posts/', include('posts.urls')),
    path('subreddits/', include('subreddits.urls')),
    path('pg-rental/', include('pg_rental.urls')),
    path('delhi-wiki/', include('delhi_wiki.urls')),
    path('bus/', include('bus_service.urls')),
    path('coupons/', include('coupon_service.urls')),
    path('metro/', include('metro.urls')),
    path('medical/', include('medical.urls')),
    path('hotel/', include('hotel_service.urls')),
    path('jobs/', include('job_portal.urls')),
    path('lost-and-found/', include('lost_and_found.urls')),
    path('storytelling/', include('storytelling.urls')),
    path('news/', include('news.urls')),
    path('notifications/', include('notifications.urls')),
    path('events/', include('events.urls', namespace='events')),
    path('pandits/', include('pandits.urls', namespace='pandits')),
    path('mithila_pride/', include('mithila_pride.urls', namespace='mithila_pride')),
    path('store/', include('store.urls', namespace='store')),
    path('cab-auto/', include('cab_auto.urls', namespace='cab_auto')),
    path('ghatkaiti/', include('ghatkaiti.urls', namespace='ghatkaiti')),
    path('mithila-panchang/', include('mithila_panchang.urls', namespace='mithila_panchang')),
    path('mithila-songs/', mithila_songs_list, name='mithila_songs_direct'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)