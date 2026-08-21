from django.urls import path
from core import admin_views, admin_seo_views

app_name = 'admin_panel'

urlpatterns = [
    # 1. Dashboard
    path('', admin_views.admin_dashboard_view, name='dashboard'),
    
    # 2. Analytics
    path('analytics/', admin_views.admin_analytics_view, name='analytics'),
    
    # 3. Users Management
    path('users/', admin_views.admin_users_list_view, name='users'),
    path('users/<int:user_id>/', admin_views.admin_user_detail_view, name='user_detail'),
    
    # 4. Submissions & Approval Queue
    path('submissions/', admin_views.admin_submissions_list_view, name='submissions'),
    path('submissions/<str:app_name>/<int:item_id>/<str:action>/', admin_views.admin_submission_action_view, name='submission_action'),
    
    # 5. Content Management
    path('news/', admin_views.admin_news_view, name='news'),
    path('stories/', admin_views.admin_stories_view, name='stories'),
    path('events/', admin_views.admin_events_view, name='events'),
    path('panchang/', admin_views.admin_panchang_view, name='panchang'),
    path('mithila-pride/', admin_views.admin_pride_view, name='pride'),
    path('pandits/', admin_views.admin_pandits_view, name='pandits'),
    path('music/', admin_views.admin_music_view, name='music'),
    
    # 6. Community & Moderation
    path('communities/', admin_views.admin_communities_view, name='communities'),
    path('communities/top/', admin_views.admin_top_communities_view, name='top_communities'),
    path('posts/', admin_views.admin_posts_view, name='posts'),
    path('comments/', admin_views.admin_comments_view, name='comments'),
    path('reports/', admin_views.admin_reports_view, name='reports'),
    
    # 7. Store & E-Commerce Suite
    path('store/', admin_views.admin_store_dashboard_view, name='store_dashboard'),
    path('store/orders/', admin_views.admin_store_orders_view, name='store_orders'),
    
    # 8. Services Marketplace
    path('services/', admin_views.admin_services_view, name='services'),
    
    # 9. System, Broadcast, CMS & Settings
    path('notifications/', admin_views.admin_notifications_view, name='notifications'),
    path('homepage/', admin_views.admin_homepage_cms_view, name='homepage'),
    path('logs/', admin_views.admin_activity_logs_view, name='logs'),
    path('settings/', admin_views.admin_settings_view, name='settings'),
    path('footer/', admin_views.admin_footer_settings_view, name='footer_settings'),

    # 10. SEO & Digital Marketing Suite
    path('seo/', admin_seo_views.admin_seo_dashboard_view, name='seo_dashboard'),
    path('seo/gsc/', admin_seo_views.admin_search_console_view, name='gsc'),
    path('seo/pages/', admin_seo_views.admin_seo_pages_view, name='seo_pages'),
    path('seo/auditor/', admin_seo_views.admin_content_seo_auditor_view, name='seo_auditor'),
    path('seo/sitemap/', admin_seo_views.admin_sitemap_view, name='sitemap'),
    path('seo/robots/', admin_seo_views.admin_robots_txt_view, name='robots'),
    path('seo/marketing/', admin_seo_views.admin_marketing_dashboard_view, name='marketing'),
    path('seo/campaigns/', admin_seo_views.admin_campaigns_view, name='campaigns'),
    path('seo/utm-builder/', admin_seo_views.admin_utm_builder_view, name='utm'),
    path('seo/social/', admin_seo_views.admin_social_view, name='social'),
    path('seo/alerts/', admin_seo_views.admin_seo_alerts_view, name='seo_alerts'),
    path('seo/reports/', admin_seo_views.admin_marketing_reports_view, name='reports_marketing'),
]

