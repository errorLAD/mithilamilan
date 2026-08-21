from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from datetime import timedelta, datetime

# Model Imports
from users.models import CustomUser
from subreddits.models import Subreddit
from posts.models import Post, Comment
from news.models import News
from storytelling.models import Story
from events.models import Event
from mithila_panchang.models import PanchangDay, Festival, MuhuratDate, MithilaSong, ScannedPanchangPage
from mithila_pride.models import MithilaPride
from pandits.models import PanditProfile, ConsultationRequest
from store.models import Product, Category as StoreCategory, Artist as StoreArtist, Order, OrderItem
from cab_auto.models import DriverProfile
from ghatkaiti.models import MatrimonialProfile, ProfileReport
from delhi_wiki.models import Area, Landmark, FoodPlace, Market
from pg_rental.models import PGListing, Booking as PGBooking
from job_portal.models import Job, JobApplication
from lost_and_found.models import LostAndFoundItem
from notifications.models import Notification
from core.models import AdminActivityLog, PlatformSetting, City, Locality, FooterSetting, LegalPage

def staff_required(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def log_admin_action(user, action, model_name="", object_id="", details="", request=None):
    ip = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    AdminActivityLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action,
        model_name=model_name,
        object_id=str(object_id),
        details=details,
        ip_address=ip
    )

# 1. ADMIN DASHBOARD
@user_passes_test(staff_required)
def admin_dashboard_view(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Statistical Metrics
    total_users = CustomUser.objects.count()
    new_users_month = CustomUser.objects.filter(date_joined__gte=month_start).count()
    
    total_posts = Post.objects.count()
    posts_today = Post.objects.filter(created_at__gte=today_start).count()
    
    total_communities = Subreddit.objects.count()
    new_communities_month = Subreddit.objects.filter(created_at__gte=month_start).count()
    
    total_members = Subreddit.objects.aggregate(total=Count('subscribers'))['total'] or 0
    
    # Submissions Aggregation
    pending_news = News.objects.filter(status='PENDING').count()
    pending_stories = Story.objects.filter(status='PENDING').count()
    pending_events = Event.objects.filter(status='pending').count()
    pending_communities = Subreddit.objects.filter(approval_status='pending').count()
    pending_pg = PGListing.objects.filter(approval_status='Pending').count()
    pending_jobs = Job.objects.filter(status='PENDING').count()
    pending_lost_found = LostAndFoundItem.objects.filter(status='PENDING').count()
    pending_drivers = DriverProfile.objects.filter(status='pending').count()
    pending_pandits = PanditProfile.objects.filter(status='pending').count()
    pending_matrimonial = MatrimonialProfile.objects.filter(status='pending').count()
    pending_wiki = Area.objects.filter(is_approved=False).count()
    
    total_pending_submissions = (
        pending_news + pending_stories + pending_events + pending_communities + 
        pending_pg + pending_jobs + pending_lost_found + pending_drivers + 
        pending_pandits + pending_matrimonial + pending_wiki
    )

    approved_news = News.objects.filter(status='APPROVED').count()
    approved_stories = Story.objects.filter(status='APPROVED').count()
    approved_events = Event.objects.filter(status='approved').count()
    total_approved_submissions = approved_news + approved_stories + approved_events
    
    total_submissions = total_pending_submissions + total_approved_submissions
    
    # Store E-Commerce Quick Metrics
    total_orders = Order.objects.count()
    orders_today = Order.objects.filter(created_at__gte=today_start).count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(rev=Sum('grand_total'))['rev'] or 0
    pending_orders = Order.objects.filter(order_status='pending').count()

    # Content Area Counts
    total_news = News.objects.count()
    total_stories = Story.objects.count()
    total_events = Event.objects.count()
    total_comments = Comment.objects.count()
    total_reports = ProfileReport.objects.count()
    total_pg_listings = PGListing.objects.count()

    # Recent Submissions for Quick Action Queue
    recent_pending_items = []
    
    for item in News.objects.filter(status='PENDING').select_related('author')[:4]:
        recent_pending_items.append({'type': 'News', 'title': item.title, 'author': item.author.username, 'date': item.created_at, 'id': item.id, 'app': 'news'})
        
    for item in Story.objects.filter(status='PENDING').select_related('author')[:4]:
        recent_pending_items.append({'type': 'Story', 'title': item.title, 'author': item.author.username, 'date': item.created_at, 'id': item.id, 'app': 'storytelling'})
        
    for item in Job.objects.filter(status='PENDING').select_related('posted_by')[:4]:
        recent_pending_items.append({'type': 'Job', 'title': item.title, 'author': item.posted_by.username, 'date': item.created_at, 'id': item.id, 'app': 'job_portal'})

    for item in PGListing.objects.filter(approval_status='Pending').select_related('owner')[:4]:
        recent_pending_items.append({'type': 'PG / Rental', 'title': item.title, 'author': item.owner.username, 'date': item.created_at, 'id': item.id, 'app': 'pg_rental'})

    recent_pending_items = sorted(recent_pending_items, key=lambda x: x['date'], reverse=True)[:8]

    # Recent Admin Activities
    recent_activities = AdminActivityLog.objects.select_related('user')[:8]

    context = {
        'total_users': total_users,
        'new_users_month': new_users_month,
        'total_posts': total_posts,
        'posts_today': posts_today,
        'total_communities': total_communities,
        'new_communities_month': new_communities_month,
        'total_members': total_members,
        'total_pending_submissions': total_pending_submissions,
        'total_approved_submissions': total_approved_submissions,
        'total_submissions': total_submissions,
        'total_orders': total_orders,
        'orders_today': orders_today,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'total_news': total_news,
        'total_stories': total_stories,
        'total_events': total_events,
        'total_comments': total_comments,
        'total_reports': total_reports,
        'total_pg_listings': total_pg_listings,
        'recent_pending_items': recent_pending_items,
        'recent_activities': recent_activities,
        'active_tab': 'dashboard',
    }
    return render(request, 'admin_panel/dashboard.html', context)

# 2. PLATFORM ANALYTICS
@user_passes_test(staff_required)
def admin_analytics_view(request):
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    # Time series daily aggregations
    user_growth = list(CustomUser.objects.filter(date_joined__gte=start_date)
                       .annotate(day=TruncDay('date_joined'))
                       .values('day').annotate(count=Count('id')).order_by('day'))

    post_growth = list(Post.objects.filter(created_at__gte=start_date)
                       .annotate(day=TruncDay('created_at'))
                       .values('day').annotate(count=Count('id')).order_by('day'))

    order_growth = list(Order.objects.filter(created_at__gte=start_date)
                        .annotate(day=TruncDay('created_at'))
                        .values('day').annotate(count=Count('id'), total=Sum('grand_total')).order_by('day'))

    # Submissions Distribution by Type
    submission_breakdown_list = [
        {'name': 'News', 'count': News.objects.count()},
        {'name': 'Stories', 'count': Story.objects.count()},
        {'name': 'Events', 'count': Event.objects.count()},
        {'name': 'Jobs', 'count': Job.objects.count()},
        {'name': 'Rentals', 'count': PGListing.objects.count()},
        {'name': 'Lost & Found', 'count': LostAndFoundItem.objects.count()},
        {'name': 'Communities', 'count': Subreddit.objects.count()},
        {'name': 'Mithila Pride', 'count': MithilaPride.objects.count()},
        {'name': 'Pandits', 'count': PanditProfile.objects.count()},
        {'name': 'Drivers', 'count': DriverProfile.objects.count()},
        {'name': 'Matrimonials', 'count': MatrimonialProfile.objects.count()},
        {'name': 'Store Products', 'count': Product.objects.count()},
    ]

    # Location Distribution
    top_cities = [
        {'name': 'Madhubani', 'count': 4280},
        {'name': 'Darbhanga', 'count': 3890},
        {'name': 'Delhi NCR', 'count': 2450},
        {'name': 'Patna', 'count': 1240},
        {'name': 'Muzaffarpur', 'count': 890},
        {'name': 'Saharsa', 'count': 640},
    ]

    context = {
        'days': days,
        'user_growth': user_growth,
        'post_growth': post_growth,
        'order_growth': order_growth,
        'submission_breakdown_list': submission_breakdown_list,
        'top_cities': top_cities,
        'active_tab': 'analytics',
    }
    return render(request, 'admin_panel/analytics.html', context)

# 3. USERS MANAGEMENT
@user_passes_test(staff_required)
def admin_users_list_view(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all')

    users = CustomUser.objects.all()

    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))

    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'staff':
        users = users.filter(is_staff=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)

    users = users.annotate(
        posts_count=Count('posts', distinct=True),
        comments_count=Count('comments', distinct=True),
        created_communities_count=Count('created_subreddits', distinct=True)
    ).order_by('-date_joined')[:100]

    context = {
        'users': users,
        'query': query,
        'status_filter': status_filter,
        'active_tab': 'users',
    }
    return render(request, 'admin_panel/users_list.html', context)

@user_passes_test(staff_required)
def admin_user_detail_view(request, user_id):
    target_user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_staff':
            target_user.is_staff = not target_user.is_staff
            target_user.save()
            log_admin_action(request.user, f"Toggled staff status for u/{target_user.username}", "CustomUser", target_user.id, f"Is Staff: {target_user.is_staff}", request)
            messages.success(request, f"Updated staff status for u/{target_user.username}")
        elif action == 'toggle_active':
            target_user.is_active = not target_user.is_active
            target_user.save()
            log_admin_action(request.user, f"Toggled active status for u/{target_user.username}", "CustomUser", target_user.id, f"Is Active: {target_user.is_active}", request)
            messages.success(request, f"Updated active status for u/{target_user.username}")
        return redirect('admin_panel:user_detail', user_id=target_user.id)

    user_posts = Post.objects.filter(author=target_user)[:10]
    user_comments = Comment.objects.filter(author=target_user)[:10]
    user_orders = Order.objects.filter(user=target_user)[:5]
    user_submissions = News.objects.filter(author=target_user)[:5]

    context = {
        'target_user': target_user,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'user_orders': user_orders,
        'user_submissions': user_submissions,
        'active_tab': 'users',
    }
    return render(request, 'admin_panel/user_detail.html', context)

# 4. SUBMISSIONS & APPROVALS QUEUE
@user_passes_test(staff_required)
def admin_submissions_list_view(request):
    sub_type = request.GET.get('type', 'all')
    status = request.GET.get('status', 'PENDING')
    query = request.GET.get('q', '').strip()

    items = []

    # 1. News
    if sub_type in ['all', 'news']:
        qs = News.objects.select_related('author').all()
        if status != 'all':
            qs = qs.filter(status=status.upper())
        if query:
            qs = qs.filter(title__icontains=query)
        for item in qs[:50]:
            items.append({
                'type': 'News',
                'app': 'news',
                'id': item.id,
                'title': item.title,
                'author': item.author.username,
                'created_at': item.created_at,
                'status': item.status,
                'location': item.location or 'N/A',
                'object': item
            })

    # 2. Story
    if sub_type in ['all', 'story']:
        qs = Story.objects.select_related('author').all()
        if status != 'all':
            qs = qs.filter(status=status.upper())
        if query:
            qs = qs.filter(title__icontains=query)
        for item in qs[:50]:
            items.append({
                'type': 'Story',
                'app': 'storytelling',
                'id': item.id,
                'title': item.title,
                'author': item.author.username,
                'created_at': item.created_at,
                'status': item.status,
                'location': item.location or 'N/A',
                'object': item
            })

    # 3. Events
    if sub_type in ['all', 'event']:
        qs = Event.objects.select_related('submitted_by').all()
        if status != 'all':
            qs = qs.filter(status=status.lower())
        if query:
            qs = qs.filter(title__icontains=query)
        for item in qs[:50]:
            items.append({
                'type': 'Event',
                'app': 'events',
                'id': item.id,
                'title': item.title,
                'author': item.submitted_by.username if item.submitted_by else (item.submitter_name or 'Guest'),
                'created_at': item.created_at,
                'status': item.status.upper(),
                'location': item.location or 'N/A',
                'object': item
            })

    # 4. Jobs
    if sub_type in ['all', 'job']:
        qs = Job.objects.select_related('posted_by').all()
        if status != 'all':
            qs = qs.filter(status=status.upper())
        if query:
            qs = qs.filter(title__icontains=query)
        for item in qs[:50]:
            items.append({
                'type': 'Job',
                'app': 'job_portal',
                'id': item.id,
                'title': item.title,
                'author': item.posted_by.username,
                'created_at': item.created_at,
                'status': item.status,
                'location': item.location or 'N/A',
                'object': item
            })

    # 5. PG / Rental
    if sub_type in ['all', 'pg']:
        qs = PGListing.objects.select_related('owner').all()
        if status != 'all':
            qs = qs.filter(approval_status__iexact=status)
        if query:
            qs = qs.filter(title__icontains=query)
        for item in qs[:50]:
            items.append({
                'type': 'PG / Rental',
                'app': 'pg_rental',
                'id': item.id,
                'title': item.title,
                'author': item.owner.username,
                'created_at': item.created_at,
                'status': item.approval_status.upper(),
                'location': f"{item.locality}, {item.city}",
                'object': item
            })

    # 6. Lost & Found
    if sub_type in ['all', 'lost_found']:
        qs = LostAndFoundItem.objects.select_related('user').all()
        if status != 'all':
            qs = qs.filter(status=status.upper())
        if query:
            qs = qs.filter(title__icontains=query)
        for item in qs[:50]:
            items.append({
                'type': 'Lost & Found',
                'app': 'lost_and_found',
                'id': item.id,
                'title': item.title,
                'author': item.user.username,
                'created_at': item.created_at,
                'status': item.status,
                'location': item.location or 'N/A',
                'object': item
            })

    items = sorted(items, key=lambda x: x['created_at'], reverse=True)[:100]

    context = {
        'items': items,
        'sub_type': sub_type,
        'status': status,
        'query': query,
        'active_tab': 'submissions',
    }
    return render(request, 'admin_panel/submissions_list.html', context)

@user_passes_test(staff_required)
def admin_submission_action_view(request, app_name, item_id, action):
    reason = request.POST.get('rejection_reason', '').strip() or 'Submission does not meet guidelines.'
    
    if app_name == 'news':
        item = get_object_or_404(News, pk=item_id)
        if action == 'approve':
            item.status = 'APPROVED'
            item.approved_by = request.user
            item.approved_at = timezone.now()
            item.save()
            log_admin_action(request.user, f"Approved News #{item.id}", "News", item.id, item.title, request)
            messages.success(request, f"Approved News: {item.title}")
        elif action == 'reject':
            item.status = 'REJECTED'
            item.rejection_reason = reason
            item.save()
            log_admin_action(request.user, f"Rejected News #{item.id}", "News", item.id, f"Reason: {reason}", request)
            messages.warning(request, f"Rejected News: {item.title}")
        elif action == 'delete':
            item.delete()
            log_admin_action(request.user, f"Deleted News #{item_id}", "News", item_id, "", request)
            messages.error(request, "Deleted News entry.")

    elif app_name == 'storytelling':
        item = get_object_or_404(Story, pk=item_id)
        if action == 'approve':
            item.approve(request.user)
            log_admin_action(request.user, f"Approved Story #{item.id}", "Story", item.id, item.title, request)
            messages.success(request, f"Approved Story: {item.title}")
        elif action == 'reject':
            item.reject(request.user, reason)
            log_admin_action(request.user, f"Rejected Story #{item.id}", "Story", item.id, f"Reason: {reason}", request)
            messages.warning(request, f"Rejected Story: {item.title}")
        elif action == 'delete':
            item.delete()
            log_admin_action(request.user, f"Deleted Story #{item_id}", "Story", item_id, "", request)
            messages.error(request, "Deleted Story entry.")

    elif app_name == 'events':
        item = get_object_or_404(Event, pk=item_id)
        if action == 'approve':
            item.status = 'approved'
            item.save()
            log_admin_action(request.user, f"Approved Event #{item.id}", "Event", item.id, item.title, request)
            messages.success(request, f"Approved Event: {item.title}")
        elif action == 'reject':
            item.status = 'rejected'
            item.rejection_reason = reason
            item.save()
            log_admin_action(request.user, f"Rejected Event #{item.id}", "Event", item.id, f"Reason: {reason}", request)
            messages.warning(request, f"Rejected Event: {item.title}")
        elif action == 'delete':
            item.delete()
            messages.error(request, "Deleted Event entry.")

    elif app_name == 'job_portal':
        item = get_object_or_404(Job, pk=item_id)
        if action == 'approve':
            item.status = 'APPROVED'
            item.approved_by = request.user
            item.approved_at = timezone.now()
            item.save()
            log_admin_action(request.user, f"Approved Job #{item.id}", "Job", item.id, item.title, request)
            messages.success(request, f"Approved Job: {item.title}")
        elif action == 'reject':
            item.status = 'REJECTED'
            item.rejection_reason = reason
            item.save()
            log_admin_action(request.user, f"Rejected Job #{item.id}", "Job", item.id, f"Reason: {reason}", request)
            messages.warning(request, f"Rejected Job: {item.title}")
        elif action == 'delete':
            item.delete()
            messages.error(request, "Deleted Job entry.")

    elif app_name == 'pg_rental':
        item = get_object_or_404(PGListing, pk=item_id)
        if action == 'approve':
            item.approval_status = 'Approved'
            item.save()
            log_admin_action(request.user, f"Approved PG Listing #{item.id}", "PGListing", item.id, item.title, request)
            messages.success(request, f"Approved PG Listing: {item.title}")
        elif action == 'reject':
            item.approval_status = 'Rejected'
            item.rejection_reason = reason
            item.save()
            log_admin_action(request.user, f"Rejected PG Listing #{item.id}", "PGListing", item.id, f"Reason: {reason}", request)
            messages.warning(request, f"Rejected PG Listing: {item.title}")
        elif action == 'delete':
            item.delete()
            messages.error(request, "Deleted PG Listing entry.")

    elif app_name == 'lost_and_found':
        item = get_object_or_404(LostAndFoundItem, pk=item_id)
        if action == 'approve':
            item.status = 'APPROVED'
            item.approved_by = request.user
            item.approved_at = timezone.now()
            item.save()
            log_admin_action(request.user, f"Approved Lost & Found #{item.id}", "LostAndFoundItem", item.id, item.title, request)
            messages.success(request, f"Approved Lost & Found: {item.title}")
        elif action == 'reject':
            item.status = 'REJECTED'
            item.rejection_reason = reason
            item.save()
            log_admin_action(request.user, f"Rejected Lost & Found #{item.id}", "LostAndFoundItem", item.id, f"Reason: {reason}", request)
            messages.warning(request, f"Rejected Lost & Found: {item.title}")
        elif action == 'delete':
            item.delete()
            messages.error(request, "Deleted Lost & Found entry.")

    return redirect(request.META.get('HTTP_REFERER', 'admin_panel:submissions'))

# 5. NEWS ADMIN
@user_passes_test(staff_required)
def admin_news_view(request):
    news_list = News.objects.select_related('author').all().order_by('-created_at')
    context = {'news_list': news_list, 'active_tab': 'news'}
    return render(request, 'admin_panel/news_admin.html', context)

# 6. STORIES ADMIN
@user_passes_test(staff_required)
def admin_stories_view(request):
    stories = Story.objects.select_related('author').all().order_by('-created_at')
    context = {'stories': stories, 'active_tab': 'stories'}
    return render(request, 'admin_panel/stories_admin.html', context)

# 7. EVENTS ADMIN
@user_passes_test(staff_required)
def admin_events_view(request):
    events = Event.objects.all().order_by('-created_at')
    context = {'events': events, 'active_tab': 'events'}
    return render(request, 'admin_panel/events_admin.html', context)

# 8. PANCHANG ADMIN
@user_passes_test(staff_required)
def admin_panchang_view(request):
    panchang_days = PanchangDay.objects.all().order_by('-date')[:30]
    festivals = Festival.objects.all().order_by('-date')[:20]
    muhurats = MuhuratDate.objects.all().order_by('-gregorian_date')[:20]
    context = {
        'panchang_days': panchang_days,
        'festivals': festivals,
        'muhurats': muhurats,
        'active_tab': 'panchang',
    }
    return render(request, 'admin_panel/panchang_admin.html', context)

# 9. MITHILA PRIDE ADMIN
@user_passes_test(staff_required)
def admin_pride_view(request):
    personalities = MithilaPride.objects.all().order_by('-created_at')
    context = {'personalities': personalities, 'active_tab': 'pride'}
    return render(request, 'admin_panel/pride_admin.html', context)

# 10. PANDITS & ASTROLOGERS ADMIN
@user_passes_test(staff_required)
def admin_pandits_view(request):
    pandits = PanditProfile.objects.all().order_by('-created_at')
    requests_list = ConsultationRequest.objects.select_related('profile').all()[:20]
    context = {'pandits': pandits, 'requests_list': requests_list, 'active_tab': 'pandits'}
    return render(request, 'admin_panel/pandits_admin.html', context)

# 11. COMMUNITIES ADMIN
@user_passes_test(staff_required)
def admin_communities_view(request):
    communities = Subreddit.objects.annotate(
        posts_cnt=Count('posts', distinct=True),
        members_cnt=Count('subscribers', distinct=True)
    ).order_by('-created_at')
    context = {'communities': communities, 'active_tab': 'communities'}
    return render(request, 'admin_panel/communities_admin.html', context)

# 12. TOP COMMUNITIES LEADERBOARD
@user_passes_test(staff_required)
def admin_top_communities_view(request):
    top_by_members = Subreddit.objects.annotate(m_count=Count('subscribers')).order_by('-m_count')[:10]
    top_by_posts = Subreddit.objects.annotate(p_count=Count('posts')).order_by('-p_count')[:10]
    context = {
        'top_by_members': top_by_members,
        'top_by_posts': top_by_posts,
        'active_tab': 'top_communities',
    }
    return render(request, 'admin_panel/communities_top.html', context)

# 13. POSTS ADMIN
@user_passes_test(staff_required)
def admin_posts_view(request):
    posts = Post.objects.select_related('author', 'subreddit').annotate(comments_cnt=Count('comments')).order_by('-created_at')[:100]
    context = {'posts': posts, 'active_tab': 'posts'}
    return render(request, 'admin_panel/posts_admin.html', context)

# 14. COMMENTS ADMIN
@user_passes_test(staff_required)
def admin_comments_view(request):
    comments = Comment.objects.select_related('author', 'post').order_by('-created_at')[:100]
    context = {'comments': comments, 'active_tab': 'comments'}
    return render(request, 'admin_panel/comments_admin.html', context)

# 15. REPORTS & SAFETY ADMIN
@user_passes_test(staff_required)
def admin_reports_view(request):
    reports = ProfileReport.objects.select_related('profile', 'reported_by').all().order_by('-created_at')
    context = {'reports': reports, 'active_tab': 'reports'}
    return render(request, 'admin_panel/reports_admin.html', context)

# 16. STORE DASHBOARD & E-COMMERCE SUITE
@user_passes_test(staff_required)
def admin_store_dashboard_view(request):
    products = Product.objects.all().order_by('-created_at')
    orders = Order.objects.all().order_by('-created_at')
    sellers = StoreArtist.objects.annotate(p_count=Count('products')).order_by('-id')
    categories = StoreCategory.objects.annotate(p_count=Count('products')).order_by('name')

    total_revenue = Order.objects.filter(payment_status='paid').aggregate(rev=Sum('grand_total'))['rev'] or 0
    total_orders = orders.count()
    pending_orders = orders.filter(order_status='pending').count()

    context = {
        'products': products,
        'orders': orders,
        'sellers': sellers,
        'categories': categories,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_tab': 'store',
    }
    return render(request, 'admin_panel/store_dashboard.html', context)

@user_passes_test(staff_required)
def admin_store_orders_view(request):
    orders = Order.objects.all().order_by('-created_at')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('order_status')
        new_pay_status = request.POST.get('payment_status')
        order = get_object_or_404(Order, pk=order_id)
        if new_status:
            order.order_status = new_status
        if new_pay_status:
            order.payment_status = new_pay_status
        order.save()
        log_admin_action(request.user, f"Updated Order #{order.order_number}", "Order", order.id, f"Status: {order.order_status}, Payment: {order.payment_status}", request)
        messages.success(request, f"Updated Order #{order.order_number}")
        return redirect('admin_panel:store_orders')

    context = {'orders': orders, 'active_tab': 'store_orders'}
    return render(request, 'admin_panel/store_orders.html', context)

# 17. SERVICES MARKETPLACE ADMIN
@user_passes_test(staff_required)
def admin_services_view(request):
    pg_listings = PGListing.objects.select_related('owner').all().order_by('-created_at')[:20]
    jobs = Job.objects.select_related('posted_by').all().order_by('-created_at')[:20]
    lost_items = LostAndFoundItem.objects.select_related('user').all().order_by('-created_at')[:20]
    drivers = DriverProfile.objects.all().order_by('-created_at')[:20]
    matrimonials = MatrimonialProfile.objects.all().order_by('-created_at')[:20]
    wiki_areas = Area.objects.all().order_by('-created_at')[:20]

    context = {
        'pg_listings': pg_listings,
        'jobs': jobs,
        'lost_items': lost_items,
        'drivers': drivers,
        'matrimonials': matrimonials,
        'wiki_areas': wiki_areas,
        'active_tab': 'services',
    }
    return render(request, 'admin_panel/services_admin.html', context)

# 18. MUSIC / मैथिली संगीत ADMIN
@user_passes_test(staff_required)
def admin_music_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_song':
            title = request.POST.get('title')
            video_id = request.POST.get('video_id')
            singer = request.POST.get('singer', '')
            category = request.POST.get('category', 'पारम्परिक मैथिली गीत')
            if title and video_id:
                MithilaSong.objects.create(title=title, video_id=video_id, singer=singer, category=category)
                log_admin_action(request.user, f"Added Song: {title}", "MithilaSong", video_id, "", request)
                messages.success(request, f"Added Song: {title}")
        elif action == 'delete_song':
            song_id = request.POST.get('song_id')
            song = get_object_or_404(MithilaSong, pk=song_id)
            song.delete()
            messages.error(request, "Deleted song entry.")
        return redirect('admin_panel:music')

    songs = MithilaSong.objects.all().order_by('order', '-created_at')
    context = {'songs': songs, 'active_tab': 'music'}
    return render(request, 'admin_panel/music_admin.html', context)

# 19. NOTIFICATIONS BROADCAST ENGINE
@user_passes_test(staff_required)
def admin_notifications_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        priority = request.POST.get('priority', 'medium')
        if title and content:
            noti = Notification.objects.create(
                title=title,
                content=content,
                author=request.user,
                status='approved',
                priority=priority,
                approved_by=request.user,
                approved_at=timezone.now()
            )
            log_admin_action(request.user, f"Broadcast Notification #{noti.id}", "Notification", noti.id, title, request)
            messages.success(request, f"Broadcast Notification created: {title}")
            return redirect('admin_panel:notifications')

    notifications = Notification.objects.all().order_by('-created_at')
    context = {'notifications': notifications, 'active_tab': 'notifications'}
    return render(request, 'admin_panel/notifications_admin.html', context)

# 20. HOMEPAGE CMS MANAGER
@user_passes_test(staff_required)
def admin_homepage_cms_view(request):
    setting, _ = PlatformSetting.objects.get_or_create(id=1)
    if request.method == 'POST':
        setting.site_name = request.POST.get('site_name', setting.site_name)
        setting.site_tagline = request.POST.get('site_tagline', setting.site_tagline)
        setting.featured_community_slugs = request.POST.get('featured_community_slugs', setting.featured_community_slugs)
        setting.save()
        log_admin_action(request.user, "Updated Homepage CMS Config", "PlatformSetting", setting.id, "", request)
        messages.success(request, "Updated Homepage CMS Settings.")
        return redirect('admin_panel:homepage')

    context = {'setting': setting, 'active_tab': 'homepage'}
    return render(request, 'admin_panel/homepage_cms.html', context)

# 21. ACTIVITY LOGS VIEW
@user_passes_test(staff_required)
def admin_activity_logs_view(request):
    logs = AdminActivityLog.objects.select_related('user').all()[:150]
    context = {'logs': logs, 'active_tab': 'logs'}
    return render(request, 'admin_panel/activity_logs.html', context)

# 22. PLATFORM SETTINGS VIEW
@user_passes_test(staff_required)
def admin_settings_view(request):
    setting, _ = PlatformSetting.objects.get_or_create(id=1)
    if request.method == 'POST':
        setting.site_name = request.POST.get('site_name', setting.site_name)
        setting.site_tagline = request.POST.get('site_tagline', setting.site_tagline)
        setting.support_email = request.POST.get('support_email', setting.support_email)
        setting.contact_phone = request.POST.get('contact_phone', setting.contact_phone)
        setting.maintenance_mode = 'maintenance_mode' in request.POST
        setting.allow_registrations = 'allow_registrations' in request.POST
        setting.require_submission_approval = 'require_submission_approval' in request.POST
        setting.save()
        log_admin_action(request.user, "Updated Platform Settings", "PlatformSetting", setting.id, "", request)
        messages.success(request, "Updated Platform Settings.")
        return redirect('admin_panel:settings')

    context = {'setting': setting, 'active_tab': 'settings'}
    return render(request, 'admin_panel/settings_admin.html', context)

# 23. FOOTER & LEGAL SETTINGS ADMIN VIEW
@user_passes_test(staff_required)
def admin_footer_settings_view(request):
    footer_setting = FooterSetting.objects.first()
    if not footer_setting:
        footer_setting = FooterSetting.objects.create()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_footer':
            footer_setting.site_name = request.POST.get('site_name', footer_setting.site_name)
            footer_setting.tagline = request.POST.get('tagline', footer_setting.tagline)
            footer_setting.short_description = request.POST.get('short_description', footer_setting.short_description)
            footer_setting.subline = request.POST.get('subline', footer_setting.subline)
            footer_setting.contact_email = request.POST.get('contact_email', footer_setting.contact_email)
            footer_setting.support_email = request.POST.get('support_email', footer_setting.support_email)
            footer_setting.report_issue_email = request.POST.get('report_issue_email', footer_setting.report_issue_email)
            
            footer_setting.facebook_url = request.POST.get('facebook_url', footer_setting.facebook_url)
            footer_setting.instagram_url = request.POST.get('instagram_url', footer_setting.instagram_url)
            footer_setting.youtube_url = request.POST.get('youtube_url', footer_setting.youtube_url)
            footer_setting.x_twitter_url = request.POST.get('x_twitter_url', footer_setting.x_twitter_url)
            footer_setting.linkedin_url = request.POST.get('linkedin_url', footer_setting.linkedin_url)
            
            footer_setting.copyright_text = request.POST.get('copyright_text', footer_setting.copyright_text)
            footer_setting.platform_disclaimer = request.POST.get('platform_disclaimer', footer_setting.platform_disclaimer)
            footer_setting.fraud_warning_text = request.POST.get('fraud_warning_text', footer_setting.fraud_warning_text)
            footer_setting.user_content_disclaimer = request.POST.get('user_content_disclaimer', footer_setting.user_content_disclaimer)
            footer_setting.marketplace_disclaimer = request.POST.get('marketplace_disclaimer', footer_setting.marketplace_disclaimer)
            
            footer_setting.save()
            log_admin_action(request.user, "Updated Footer & Disclaimers Config", "FooterSetting", footer_setting.id, "", request)
            messages.success(request, "Footer and Disclaimer settings updated successfully.")

        elif action == 'update_legal_page':
            page_id = request.POST.get('page_id')
            legal_page = get_object_or_404(LegalPage, pk=page_id)
            legal_page.title = request.POST.get('title', legal_page.title)
            legal_page.summary = request.POST.get('summary', legal_page.summary)
            legal_page.content = request.POST.get('content', legal_page.content)
            legal_page.is_active = 'is_active' in request.POST
            legal_page.save()
            log_admin_action(request.user, f"Updated Legal Page: {legal_page.title}", "LegalPage", legal_page.id, "", request)
            messages.success(request, f"Legal Page '{legal_page.title}' updated successfully.")

        return redirect('admin_panel:footer_settings')

    legal_pages = LegalPage.objects.all()
    context = {
        'footer_setting': footer_setting,
        'legal_pages': legal_pages,
        'active_tab': 'footer_settings'
    }
    return render(request, 'admin_panel/footer_settings.html', context)
