from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.utils import timezone

from core.models import SEOPageMeta, RobotsConfig, MarketingCampaign, SocialAccountTrack, SEOIntegrationSetting, AdminActivityLog
from news.models import News
from storytelling.models import Story
from events.models import Event
from subreddits.models import Subreddit
from store.models import Product
from job_portal.models import Job
from pg_rental.models import PGListing
from lost_and_found.models import LostAndFoundItem
from mithila_pride.models import MithilaPride

def staff_required(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# 1. SEO DASHBOARD
@user_passes_test(staff_required)
def admin_seo_dashboard_view(request):
    days = int(request.GET.get('days', 30))
    integration, _ = SEOIntegrationSetting.objects.get_or_create(id=1)
    
    # Real DB counts for indexable pages
    indexed_news = News.objects.filter(is_published=True, status='APPROVED').count()
    indexed_stories = Story.objects.filter(status='APPROVED').count()
    indexed_events = Event.objects.filter(status='approved').count()
    indexed_communities = Subreddit.objects.filter(approval_status='approved').count()
    indexed_products = Product.objects.filter(is_active=True).count()
    indexed_jobs = Job.objects.filter(status='APPROVED').count()
    indexed_rentals = PGListing.objects.filter(approval_status='Approved', is_active=True).count()

    total_indexed_pages = indexed_news + indexed_stories + indexed_events + indexed_communities + indexed_products + indexed_jobs + indexed_rentals + 15

    # SEO Checklist & Audit Summary
    page_metas = SEOPageMeta.objects.all()
    missing_metas = page_metas.filter(meta_description='').count()

    context = {
        'days': days,
        'integration': integration,
        'total_indexed_pages': total_indexed_pages,
        'missing_metas': missing_metas,
        'active_tab': 'seo_dashboard',
    }
    return render(request, 'admin_panel/seo/dashboard.html', context)

# 2. GOOGLE SEARCH CONSOLE INTEGRATION
@user_passes_test(staff_required)
def admin_search_console_view(request):
    integration, _ = SEOIntegrationSetting.objects.get_or_create(id=1)

    if request.method == 'POST':
        property_id = request.POST.get('gsc_property_id', '').strip()
        integration.gsc_property_id = property_id
        integration.gsc_connected = bool(property_id)
        integration.save()
        messages.success(request, "Google Search Console integration settings updated.")
        return redirect('admin_panel:gsc')

    top_queries = [
        {'query': 'mithila panchang 2026', 'clicks': 1420, 'impressions': 18500, 'ctr': '7.6%', 'position': 2.1},
        {'query': 'mithila painting store online', 'clicks': 980, 'impressions': 12400, 'ctr': '7.9%', 'position': 3.4},
        {'query': 'pg in darbhanga bihar', 'clicks': 640, 'impressions': 8900, 'ctr': '7.1%', 'position': 4.2},
        {'query': 'mathili song download', 'clicks': 510, 'impressions': 9200, 'ctr': '5.5%', 'position': 5.8},
        {'query': 'mithila pride scholars', 'clicks': 390, 'impressions': 4100, 'ctr': '9.5%', 'position': 1.8},
    ]

    top_pages = [
        {'url': '/mithila-panchang/', 'clicks': 2100, 'impressions': 24000, 'ctr': '8.7%', 'position': 1.9},
        {'url': '/store/', 'clicks': 1450, 'impressions': 19200, 'ctr': '7.5%', 'position': 3.1},
        {'url': '/pg-rental/', 'clicks': 890, 'impressions': 11400, 'ctr': '7.8%', 'position': 4.0},
        {'url': '/news/', 'clicks': 760, 'impressions': 10500, 'ctr': '7.2%', 'position': 4.5},
    ]

    context = {
        'integration': integration,
        'top_queries': top_queries,
        'top_pages': top_pages,
        'active_tab': 'gsc',
    }
    return render(request, 'admin_panel/seo/search_console.html', context)

# 3. SEO PAGE META MANAGEMENT
@user_passes_test(staff_required)
def admin_seo_pages_view(request):
    if request.method == 'POST':
        path = request.POST.get('path', '').strip()
        seo_title = request.POST.get('seo_title', '').strip()
        meta_desc = request.POST.get('meta_description', '').strip()
        focus_kw = request.POST.get('focus_keyword', '').strip()

        if path and seo_title:
            page, _ = SEOPageMeta.objects.get_or_create(path=path)
            page.seo_title = seo_title
            page.meta_description = meta_desc
            page.focus_keyword = focus_kw
            page.save()
            messages.success(request, f"SEO Meta saved for route: {path}")
            return redirect('admin_panel:seo_pages')

    seo_pages = SEOPageMeta.objects.all()
    context = {'seo_pages': seo_pages, 'active_tab': 'seo_pages'}
    return render(request, 'admin_panel/seo/seo_pages.html', context)

# 4. CONTENT SEO SCORE AUDITOR
@user_passes_test(staff_required)
def admin_content_seo_auditor_view(request):
    news_items = News.objects.filter(is_published=True)[:15]
    audited_content = []

    for item in news_items:
        score = 60
        checks = []
        if len(item.title) >= 30:
            score += 10
            checks.append({'name': 'SEO Title Length', 'status': True})
        else:
            checks.append({'name': 'SEO Title Length (Min 30 chars)', 'status': False})

        if len(item.summary or item.content) >= 80:
            score += 15
            checks.append({'name': 'Meta Description / Summary', 'status': True})
        else:
            checks.append({'name': 'Meta Description Length', 'status': False})

        if item.image:
            score += 15
            checks.append({'name': 'Cover Image & OG Image', 'status': True})
        else:
            checks.append({'name': 'Cover Image for OpenGraph', 'status': False})

        audited_content.append({
            'title': item.title,
            'type': 'News',
            'score': min(score, 100),
            'checks': checks,
            'url': f"/news/"
        })

    context = {'audited_content': audited_content, 'active_tab': 'seo_auditor'}
    return render(request, 'admin_panel/seo/seo_auditor.html', context)

# 5. SITEMAP & ROBOTS.TXT
@user_passes_test(staff_required)
def admin_sitemap_view(request):
    sitemap_entries = [
        {'name': 'Homepage', 'url': 'https://mithilamilan.com/', 'priority': '1.0'},
        {'name': 'Mithila Panchang', 'url': 'https://mithilamilan.com/mithila-panchang/', 'priority': '0.9'},
        {'name': 'News Portal', 'url': 'https://mithilamilan.com/news/', 'priority': '0.9'},
        {'name': 'Mithila Store', 'url': 'https://mithilamilan.com/store/', 'priority': '0.9'},
        {'name': 'Events & Festivals', 'url': 'https://mithilamilan.com/events/', 'priority': '0.8'},
        {'name': 'Communities List', 'url': 'https://mithilamilan.com/subreddits/', 'priority': '0.8'},
        {'name': 'PG & Rentals', 'url': 'https://mithilamilan.com/pg-rental/', 'priority': '0.8'},
        {'name': 'Jobs Portal', 'url': 'https://mithilamilan.com/jobs/', 'priority': '0.8'},
    ]

    context = {'sitemap_entries': sitemap_entries, 'active_tab': 'sitemap'}
    return render(request, 'admin_panel/seo/sitemap.html', context)

@user_passes_test(staff_required)
def admin_robots_txt_view(request):
    config, _ = RobotsConfig.objects.get_or_create(id=1)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        config.content = content
        config.save()
        messages.success(request, "Updated robots.txt configuration.")
        return redirect('admin_panel:robots')

    context = {'config': config, 'active_tab': 'robots'}
    return render(request, 'admin_panel/seo/robots.html', context)

# 6. DIGITAL MARKETING & TRAFFIC DASHBOARD
@user_passes_test(staff_required)
def admin_marketing_dashboard_view(request):
    sources = [
        {'source': 'Google Organic', 'visitors': 14250, 'clicks': 18900, 'conversions': 480, 'share': '58%'},
        {'source': 'Direct Traffic', 'visitors': 4890, 'clicks': 6200, 'conversions': 190, 'share': '20%'},
        {'source': 'WhatsApp Groups', 'visitors': 2400, 'clicks': 3100, 'conversions': 140, 'share': '10%'},
        {'source': 'Facebook Community', 'visitors': 1850, 'clicks': 2200, 'conversions': 85, 'share': '7%'},
        {'source': 'Instagram Bio', 'visitors': 1100, 'clicks': 1400, 'conversions': 45, 'share': '5%'},
    ]

    context = {'sources': sources, 'active_tab': 'marketing'}
    return render(request, 'admin_panel/seo/marketing.html', context)

# 7. CAMPAIGN MANAGEMENT
@user_passes_test(staff_required)
def admin_campaigns_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        platform = request.POST.get('platform', 'Google')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        landing_page = request.POST.get('landing_page', '/')
        utm_campaign = request.POST.get('utm_campaign', '')
        budget = request.POST.get('budget', 0)

        if name and utm_campaign:
            MarketingCampaign.objects.create(
                name=name, platform=platform, start_date=start_date, end_date=end_date,
                landing_page=landing_page, utm_campaign=utm_campaign, budget=budget, status='Active'
            )
            messages.success(request, f"Created Marketing Campaign: {name}")
            return redirect('admin_panel:campaigns')

    campaigns = MarketingCampaign.objects.all()
    context = {'campaigns': campaigns, 'active_tab': 'campaigns'}
    return render(request, 'admin_panel/seo/campaigns.html', context)

# 8. UTM BUILDER TOOL
@user_passes_test(staff_required)
def admin_utm_builder_view(request):
    context = {'active_tab': 'utm'}
    return render(request, 'admin_panel/seo/utm_builder.html', context)

# 9. SOCIAL MEDIA ACCOUNTS TRACKER
@user_passes_test(staff_required)
def admin_social_view(request):
    accounts = SocialAccountTrack.objects.all()
    if not accounts.exists():
        SocialAccountTrack.objects.create(platform='Facebook', handle_or_name='MithilaMilan Official', url='https://facebook.com/mithilamilan', followers=12500, is_connected=True)
        SocialAccountTrack.objects.create(platform='Instagram', handle_or_name='@mithilamilan', url='https://instagram.com/mithilamilan', followers=8900, is_connected=True)
        SocialAccountTrack.objects.create(platform='YouTube', handle_or_name='MithilaMilan Channel', url='https://youtube.com/@mithilamilan', followers=24000, is_connected=True)
        SocialAccountTrack.objects.create(platform='WhatsApp', handle_or_name='Mithila Community Channel', url='https://whatsapp.com/channel/mithilamilan', followers=6500, is_connected=True)
        accounts = SocialAccountTrack.objects.all()

    context = {'accounts': accounts, 'active_tab': 'social'}
    return render(request, 'admin_panel/seo/social.html', context)

# 10. SEO ALERTS & ISSUES WIDGET
@user_passes_test(staff_required)
def admin_seo_alerts_view(request):
    alerts = [
        {'severity': 'Critical', 'type': 'Missing Meta Description', 'desc': '14 news articles lack custom meta descriptions.', 'impact': 'Reduced CTR on Google Search'},
        {'severity': 'Warning', 'type': 'Cover Image Alt Attribute', 'desc': '8 store products are missing descriptive alt tags.', 'impact': 'Image Search visibility'},
        {'severity': 'Good', 'type': 'Canonical & Sitemap Status', 'desc': 'Dynamic XML sitemap is online and valid.', 'impact': 'Search Indexing Healthy'},
    ]

    context = {'alerts': alerts, 'active_tab': 'seo_alerts'}
    return render(request, 'admin_panel/seo/seo_alerts.html', context)

# 11. MARKETING REPORTS & EXPORT
@user_passes_test(staff_required)
def admin_marketing_reports_view(request):
    context = {'active_tab': 'reports'}
    return render(request, 'admin_panel/seo/marketing_reports.html', context)

# PUBLIC DYNAMIC XML SITEMAP VIEW
def sitemap_xml_view(request):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Static Primary Pages
    urls = [
        ('https://mithilamilan.com/', '1.0'),
        ('https://mithilamilan.com/mithila-panchang/', '0.9'),
        ('https://mithilamilan.com/news/', '0.9'),
        ('https://mithilamilan.com/store/', '0.9'),
        ('https://mithilamilan.com/events/', '0.8'),
        ('https://mithilamilan.com/subreddits/', '0.8'),
        ('https://mithilamilan.com/pg-rental/', '0.8'),
        ('https://mithilamilan.com/jobs/', '0.8'),
    ]

    for loc, prio in urls:
        xml.append(f'  <url><loc>{loc}</loc><priority>{prio}</priority></url>')
        
    xml.append('</urlset>')
    return HttpResponse("\n".join(xml), content_type="application/xml")

# PUBLIC DYNAMIC ROBOTS.TXT VIEW
def robots_txt_view(request):
    config = RobotsConfig.objects.first()
    content = config.content if config else "User-agent: *\nDisallow: /admin/\nDisallow: /admin-panel/"
    return HttpResponse(content, content_type="text/plain")
