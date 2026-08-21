from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils import timezone
from news.models import News
from storytelling.models import Story
from pg_rental.models import PGListing
from job_portal.models import Job
from lost_and_found.models import LostAndFoundItem
from delhi_wiki.models import Landmark, Area
from events.models import Event
from pandits.models import PanditProfile
from mithila_pride.models import MithilaPride
from cab_auto.models import DriverProfile
from ghatkaiti.models import MatrimonialProfile

def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin_or_staff)
def moderation_dashboard(request):
    tab = request.GET.get('tab', 'news').strip()
    status_filter = request.GET.get('status', 'all').strip()
    query = request.GET.get('q', '').strip()

    # Global Counters Across All Content Types
    global_pending = (
        News.objects.filter(status='PENDING').count() +
        Story.objects.filter(status='PENDING').count() +
        PGListing.objects.filter(approval_status='Pending').count() +
        Job.objects.filter(status='PENDING').count() +
        LostAndFoundItem.objects.filter(status='PENDING').count()
    )

    global_approved = (
        News.objects.filter(status='APPROVED').count() +
        Story.objects.filter(status='APPROVED').count() +
        PGListing.objects.filter(approval_status='Approved').count() +
        Job.objects.filter(status='APPROVED').count() +
        LostAndFoundItem.objects.filter(status='APPROVED').count()
    )

    global_rejected = (
        News.objects.filter(status='REJECTED').count() +
        Story.objects.filter(status='REJECTED').count() +
        PGListing.objects.filter(approval_status='Rejected').count() +
        Job.objects.filter(status='REJECTED').count() +
        LostAndFoundItem.objects.filter(status='REJECTED').count()
    )

    items = []
    
    if tab == 'news':
        qs = News.objects.all()
        if status_filter == 'pending':
            qs = qs.filter(status='PENDING')
        elif status_filter == 'approved':
            qs = qs.filter(status='APPROVED')
        elif status_filter == 'rejected':
            qs = qs.filter(status='REJECTED')
        if query:
            qs = qs.filter(title__icontains=query)
        items = qs.order_by('-created_at')

    elif tab == 'stories':
        qs = Story.objects.all()
        if status_filter == 'pending':
            qs = qs.filter(status='PENDING')
        elif status_filter == 'approved':
            qs = qs.filter(status='APPROVED')
        elif status_filter == 'rejected':
            qs = qs.filter(status='REJECTED')
        if query:
            qs = qs.filter(title__icontains=query)
        items = qs.order_by('-created_at')

    elif tab == 'rentals':
        qs = PGListing.objects.all()
        if status_filter == 'pending':
            qs = qs.filter(approval_status='Pending')
        elif status_filter == 'approved':
            qs = qs.filter(approval_status='Approved')
        elif status_filter == 'rejected':
            qs = qs.filter(approval_status='Rejected')
        if query:
            qs = qs.filter(title__icontains=query)
        items = qs.order_by('-created_at')

    elif tab == 'jobs':
        qs = Job.objects.all()
        if status_filter == 'pending':
            qs = qs.filter(status='PENDING')
        elif status_filter == 'approved':
            qs = qs.filter(status='APPROVED')
        elif status_filter == 'rejected':
            qs = qs.filter(status='REJECTED')
        if query:
            qs = qs.filter(title__icontains=query)
        items = qs.order_by('-created_at')

    elif tab == 'lost_found':
        qs = LostAndFoundItem.objects.all()
        if status_filter == 'pending':
            qs = qs.filter(status='PENDING')
        elif status_filter == 'approved':
            qs = qs.filter(status='APPROVED')
        elif status_filter == 'rejected':
            qs = qs.filter(status='REJECTED')
        if query:
            qs = qs.filter(title__icontains=query)
        items = qs.order_by('-created_at')

    elif tab == 'parichay':
        qs = Landmark.objects.all()
        if status_filter == 'pending':
            qs = qs.filter(is_approved=False)
        elif status_filter == 'approved':
            qs = qs.filter(is_approved=True)
        if query:
            qs = qs.filter(name__icontains=query)
        items = qs.order_by('-created_at')

    context = {
        'active_tab': tab,
        'status_filter': status_filter,
        'query': query,
        'items': items,
        'global_pending': global_pending,
        'global_approved': global_approved,
        'global_rejected': global_rejected,
    }
    return render(request, 'core/moderation_dashboard.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
@require_POST
def moderation_action(request, item_type, pk, action):
    model_map = {
        'news': News,
        'story': Story,
        'rental': PGListing,
        'job': Job,
        'lost_found': LostAndFoundItem,
        'parichay': Landmark,
        'event': Event,
        'pandit': PanditProfile,
        'mithila_pride': MithilaPride,
        'driver': DriverProfile,
        'matrimonial': MatrimonialProfile,
    }

    model_class = model_map.get(item_type)
    if not model_class:
        messages.error(request, "invalid model type.")
        return redirect('core:moderation_dashboard')

    item = get_object_or_404(model_class, pk=pk)
    reason = request.POST.get('reason', '').strip()

    if action == 'approve':
        if hasattr(item, 'status'):
            item.status = 'APPROVED'
        if hasattr(item, 'approval_status'):
            item.approval_status = 'Approved'
        if hasattr(item, 'is_approved'):
            item.is_approved = True
        if hasattr(item, 'approved_by'):
            item.approved_by = request.user
        if hasattr(item, 'approved_at'):
            item.approved_at = timezone.now()
        item.save()
        messages.success(request, f"Approved submission '{item}' successfully.")

    elif action == 'reject':
        if hasattr(item, 'status'):
            item.status = 'REJECTED'
        if hasattr(item, 'approval_status'):
            item.approval_status = 'Rejected'
        if hasattr(item, 'is_approved'):
            item.is_approved = False
        if hasattr(item, 'rejection_reason'):
            item.rejection_reason = reason
        item.save()
        messages.warning(request, f"Rejected submission '{item}'. Reason recorded.")

    elif action == 'delete':
        title = str(item)
        item.delete()
        messages.success(request, f"Deleted '{title}'.")

    redirect_tab_map = {
        'news': 'news',
        'story': 'stories',
        'rental': 'rentals',
        'job': 'jobs',
        'lost_found': 'lost_found',
        'parichay': 'parichay',
    }
    return redirect(f"/moderation/?tab={redirect_tab_map.get(item_type, 'news')}")

@login_required
def user_submissions(request):
    user = request.user
    my_news = News.objects.filter(author=user).order_by('-created_at')
    my_stories = Story.objects.filter(author=user).order_by('-created_at')
    my_rentals = PGListing.objects.filter(owner=user).order_by('-created_at')
    my_jobs = Job.objects.filter(posted_by=user).order_by('-created_at')
    my_lost_found = LostAndFoundItem.objects.filter(user=user).order_by('-created_at')

    context = {
        'my_news': my_news,
        'my_stories': my_stories,
        'my_rentals': my_rentals,
        'my_jobs': my_jobs,
        'my_lost_found': my_lost_found,
        'total_submissions': (
            my_news.count() + my_stories.count() +
            my_rentals.count() + my_jobs.count() +
            my_lost_found.count()
        )
    }
    return render(request, 'core/user_submissions.html', context)
