from .models import City, Locality, UserLocationPreference, FooterSetting, LegalPage
from subreddits.models import Subreddit
from django.db.models import Count

def location_and_nav_context(request):
    active_city = None
    active_locality = None
    
    # Try session first
    active_city_slug = request.session.get('active_city_slug')
    if active_city_slug:
        try:
            active_city = City.objects.get(slug=active_city_slug)
        except City.DoesNotExist:
            pass
            
    # If authenticated and no session preference, try user preference
    if not active_city and request.user.is_authenticated:
        pref = getattr(request.user, 'location_preference', None)
        if pref and pref.city:
            active_city = pref.city
            request.session['active_city_slug'] = active_city.slug
            
    # Default to Delhi NCR or first popular city if available
    available_cities = list(City.objects.filter(is_popular=True))
    if not available_cities:
        available_cities = list(City.objects.all()[:10])

    popular_communities = Subreddit.objects.filter(
        approval_status='approved'
    ).annotate(member_count=Count('subscribers')).order_by('-member_count')[:6]

    modules = [
        {'name': 'होम', 'url': 'core:home', 'icon': 'fa-house', 'key': 'feed'},
        {'name': 'पावन पर्व एवं आयोजन', 'url': 'events:event_list', 'icon': 'fa-calendar-star', 'key': 'events'},
        {'name': 'मिथिला पंचांग', 'url': 'mithila_panchang:panchang_home', 'icon': 'fa-calendar-days', 'key': 'mithila_panchang'},
        {'name': 'पंडित एवं ज्योतिषी', 'url': 'pandits:profile_list', 'icon': 'fa-om', 'key': 'pandits'},
        {'name': 'मिथिला गौरव एवं विद्वान', 'url': 'mithila_pride:person_list', 'icon': 'fa-graduation-cap', 'key': 'mithila_pride'},
        {'name': 'मिथिला स्टोर', 'url': 'store:store_home', 'icon': 'fa-bag-shopping', 'key': 'store'},
        {'name': 'कैब एवं ऑटो', 'url': 'cab_auto:cab_auto_home', 'icon': 'fa-taxi', 'key': 'cab_auto'},
        {'name': 'घटकैती', 'url': 'ghatkaiti:profile_list', 'icon': 'fa-ring', 'key': 'ghatkaiti'},
        {'name': 'मिथिला परिचय', 'url': 'delhi_wiki:area_list', 'icon': 'fa-folder-closed', 'key': 'delhi_wiki'},
        {'name': 'किरायाक घर', 'url': 'pg_rental:listings', 'icon': 'fa-building', 'key': 'pg_rental'},
        {'name': 'रोजगार', 'url': 'job_portal:job_list', 'icon': 'fa-briefcase', 'key': 'job_portal'},
        {'name': 'हरायल आ भेटल वस्तु', 'url': 'lost_and_found:item_list', 'icon': 'fa-magnifying-glass', 'key': 'lost_and_found'},
        {'name': 'कहानी', 'url': 'storytelling:story_list', 'icon': 'fa-image', 'key': 'storytelling'},
        {'name': 'समाचार', 'url': 'news:news_list', 'icon': 'fa-file-lines', 'key': 'news'},
    ]

    # Footer Settings
    footer_settings = FooterSetting.objects.first()
    if not footer_settings:
        footer_settings = FooterSetting.objects.create()

    legal_pages = LegalPage.objects.filter(is_active=True)

    return {
        'active_city': active_city,
        'active_locality': active_locality,
        'available_cities': available_cities,
        'popular_communities': popular_communities,
        'platform_modules': modules,
        'footer_settings': footer_settings,
        'legal_pages': legal_pages,
    }
