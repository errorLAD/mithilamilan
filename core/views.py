from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post
from subreddits.models import Subreddit
from pg_rental.models import PGListing
from job_portal.models import Job
from news.models import News
from coupon_service.models import Coupon
from storytelling.models import Story
from lost_and_found.models import LostAndFoundItem
from datetime import date
from mithila_panchang.models import MithilaSong, PanchangDay, Festival

def home(request):
    posts = Post.objects.all().order_by('-created_at')[:20]
    subreddits = Subreddit.objects.filter(approval_status='approved').order_by('-created_at')[:6]
    featured_pgs = PGListing.objects.filter(is_active=True, approval_status='Approved').order_by('-created_at')[:4]
    featured_jobs = Job.objects.filter(status='APPROVED', is_filled=False).order_by('-created_at')[:4]
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:4]
    active_coupons = Coupon.objects.filter(is_active=True).order_by('-created_at')[:4]
    recent_stories = Story.objects.filter(status='APPROVED').order_by('-created_at')[:4]
    lost_found_items = LostAndFoundItem.objects.filter(status='APPROVED', is_resolved=False).order_by('-created_at')[:4]
    mithila_songs = MithilaSong.objects.filter(is_published=True).order_by('order')[:6]
    
    # Panchang Today & Upcoming Festival Data
    today = date.today()
    HINDI_MONTHS = {
        1: 'जनवरी', 2: 'फरवरी', 3: 'मार्च', 4: 'अप्रैल', 5: 'मई', 6: 'जून',
        7: 'जुलाई', 8: 'अगस्त', 9: 'सितंबर', 10: 'अक्टूबर', 11: 'नवंबर', 12: 'दिसंबर'
    }
    today_date_hi = f"{today.day} {HINDI_MONTHS.get(today.month, '')}"

    today_panchang = PanchangDay.objects.filter(date=today).first()
    if not today_panchang:
        today_panchang = PanchangDay.objects.filter(date__lte=today).order_by('-date').first()
        if not today_panchang:
            today_panchang = PanchangDay.objects.order_by('date').first()

    upcoming_festival = Festival.objects.filter(date__gte=today).order_by('date').first()
    if not upcoming_festival:
        upcoming_festival = Festival.objects.order_by('date').first()

    upcoming_festival_date_hi = ""
    if upcoming_festival:
        upcoming_festival_date_hi = f"{upcoming_festival.date.day} {HINDI_MONTHS.get(upcoming_festival.date.month, '')}"

    context = {
        'posts': posts,
        'subreddits': subreddits,
        'featured_pgs': featured_pgs,
        'featured_jobs': featured_jobs,
        'latest_news': latest_news,
        'active_coupons': active_coupons,
        'recent_stories': recent_stories,
        'lost_found_items': lost_found_items,
        'mithila_songs': mithila_songs,
        'today_panchang': today_panchang,
        'upcoming_festival': upcoming_festival,
        'today_date': today,
        'today_date_hi': today_date_hi,
        'upcoming_festival_date_hi': upcoming_festival_date_hi,
    }
    
    return render(request, 'core/home.html', context)

def set_location(request):
    if request.method == 'POST':
        city_slug = request.POST.get('city_slug')
        next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
        
        if city_slug == 'all' or not city_slug:
            request.session['active_city_slug'] = None
            if request.user.is_authenticated:
                UserLocationPreference.objects.filter(user=request.user).update(city=None)
            messages.info(request, "Location set to All India")
        else:
            try:
                city = City.objects.get(slug=city_slug)
                request.session['active_city_slug'] = city.slug
                if request.user.is_authenticated:
                    pref, created = UserLocationPreference.objects.get_or_create(user=request.user)
                    pref.city = city
                    pref.save()
                messages.success(request, f"Location updated to {city.name}")
            except City.DoesNotExist:
                messages.error(request, "Selected city not found.")
                
        return redirect(next_url)
    return redirect('core:home')

def about(request):
    return render(request, 'core/about.html')

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html')