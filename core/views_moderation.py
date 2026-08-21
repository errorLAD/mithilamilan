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

from django.urls import reverse
from subreddits.models import Subreddit
from posts.models import Post

def normalize_submission(item_id, cat_key, cat_name, title, created_at, updated_at=None, raw_status='PENDING', is_approved=None, rejection_reason='', content='', location='', get_url=None, edit_url=None):
    if is_approved is not None:
        norm_status = 'APPROVED' if is_approved else 'PENDING'
    else:
        s = str(raw_status).upper().strip()
        if s in ['APPROVED', 'PUBLISHED']:
            norm_status = 'APPROVED'
        elif s in ['REJECTED']:
            norm_status = 'REJECTED'
        elif s in ['NEEDS_CHANGES', 'NEEDS CHANGES']:
            norm_status = 'NEEDS_CHANGES'
        elif s in ['DRAFT']:
            norm_status = 'DRAFT'
        else:
            norm_status = 'PENDING'
    
    return {
        'id': f"{cat_key}-{item_id}",
        'item_id': item_id,
        'cat_key': cat_key,
        'cat_name': cat_name,
        'title': title or 'Untitled Submission',
        'created_at': created_at,
        'updated_at': updated_at or created_at,
        'status': norm_status,
        'rejection_reason': rejection_reason or '',
        'content': content or '',
        'location': location or '',
        'detail_url': get_url or '',
        'edit_url': edit_url or '',
    }

@login_required
def user_submissions(request):
    user = request.user

    # 1. News
    news_items = [
        normalize_submission(item.id, 'news', '📰 समाचार', item.title, item.created_at, getattr(item, 'updated_at', None), getattr(item, 'status', 'PENDING'), rejection_reason=getattr(item, 'rejection_reason', ''), content=getattr(item, 'content', ''), location=getattr(item, 'location', ''))
        for item in News.objects.filter(author=user).order_by('-created_at')
    ]

    # 2. Stories
    story_items = [
        normalize_submission(item.id, 'stories', '📖 कहानी', item.title, item.created_at, getattr(item, 'updated_at', None), getattr(item, 'status', 'PENDING'), rejection_reason=getattr(item, 'rejection_reason', ''), content=getattr(item, 'content', ''))
        for item in Story.objects.filter(author=user).order_by('-created_at')
    ]

    # 3. PG & Rentals
    rental_items = [
        normalize_submission(item.id, 'rentals', '🏠 किरायाक घर', item.title, item.created_at, getattr(item, 'updated_at', None), getattr(item, 'approval_status', 'Pending'), rejection_reason=getattr(item, 'rejection_reason', ''), content=getattr(item, 'description', ''), location=getattr(item, 'location', ''))
        for item in PGListing.objects.filter(owner=user).order_by('-created_at')
    ]

    # 4. Jobs
    job_items = [
        normalize_submission(item.id, 'jobs', '💼 रोजगार', item.title, item.created_at, getattr(item, 'updated_at', None), getattr(item, 'status', 'PENDING'), rejection_reason=getattr(item, 'rejection_reason', ''), content=getattr(item, 'description', ''), location=getattr(item, 'location', ''))
        for item in Job.objects.filter(posted_by=user).order_by('-created_at')
    ]

    # 5. Lost & Found
    lost_items = [
        normalize_submission(item.id, 'lost_found', '🔍 हरायल आ भेटल वस्तु', item.title, item.created_at, getattr(item, 'updated_at', None), getattr(item, 'status', 'PENDING'), rejection_reason=getattr(item, 'rejection_reason', ''), content=getattr(item, 'description', ''), location=getattr(item, 'location', ''))
        for item in LostAndFoundItem.objects.filter(user=user).order_by('-created_at')
    ]

    # 6. Events & Festivals
    event_items = [
        normalize_submission(item.id, 'events', '🎉 पावन पर्व एवं आयोजन', item.title, item.created_at, getattr(item, 'updated_at', None), getattr(item, 'status', 'pending'), rejection_reason=getattr(item, 'rejection_reason', ''), content=getattr(item, 'short_description', ''), location=getattr(item, 'location', ''))
        for item in Event.objects.filter(submitted_by=user).order_by('-created_at')
    ]

    # 7. Mithila Pride & Scholars
    pride_items = [
        normalize_submission(item.id, 'pride', '👨‍🎓 मिथिला गौरव एवं विद्वान', item.full_name, item.created_at, getattr(item, 'updated_at', None), getattr(item, 'status', 'pending'), rejection_reason=getattr(item, 'rejection_reason', ''), content=getattr(item, 'biography', ''), location=getattr(item, 'place_location', ''))
        for item in MithilaPride.objects.filter(submitted_by=user).order_by('-created_at')
    ]

    # 8. Pandits & Astrologers
    pandit_items = [
        normalize_submission(item.id, 'pandits', '🧑‍🦳 पंडित एवं ज्योतिषी', item.full_name, getattr(item, 'created_at', timezone.now()), getattr(item, 'created_at', timezone.now()), getattr(item, 'status', 'pending'), content=getattr(item, 'about', ''), location=getattr(item, 'location', ''))
        for item in PanditProfile.objects.filter(user=user)
    ]

    # 9. Drivers (Cab & Auto)
    driver_items = [
        normalize_submission(item.id, 'cab_auto', '🚕 कैब एवं ऑटो', item.full_name, getattr(item, 'created_at', timezone.now()), getattr(item, 'created_at', timezone.now()), getattr(item, 'status', 'pending'), content=getattr(item, 'about', ''), location=getattr(item, 'service_area', ''))
        for item in DriverProfile.objects.filter(user=user)
    ]

    # 10. Matrimonial (Ghatkaiti)
    mat_items = [
        normalize_submission(item.id, 'ghatkaiti', '👥 घटकैती', item.full_name, getattr(item, 'created_at', timezone.now()), getattr(item, 'created_at', timezone.now()), getattr(item, 'status', 'pending'), content=getattr(item, 'profession', ''), location=getattr(item, 'location', ''))
        for item in MatrimonialProfile.objects.filter(submitted_by=user)
    ]

    # 11. Mithila Parichay / Wiki
    parichay_items = [
        normalize_submission(item.id, 'parichay', '📍 मिथिला परिचय', item.name, item.created_at, getattr(item, 'updated_at', None), is_approved=item.is_approved, content=getattr(item, 'description', ''), location=getattr(item, 'address', ''))
        for item in Landmark.objects.filter(created_by=user).order_by('-created_at')
    ]

    # 12. Subreddits / Communities
    subreddit_items = [
        normalize_submission(item.id, 'subreddits', '👥 Community Requests', item.name, item.created_at, item.created_at, getattr(item, 'approval_status', 'pending'), content=getattr(item, 'description', ''))
        for item in Subreddit.objects.filter(creator=user).order_by('-created_at')
    ]

    # 13. Posts
    post_items = [
        normalize_submission(item.id, 'posts', '📝 Community Posts', item.title, item.created_at, getattr(item, 'updated_at', None), raw_status='APPROVED', content=getattr(item, 'content', ''))
        for item in Post.objects.filter(author=user).order_by('-created_at')
    ]

    def try_reverse(name, default_url='#'):
        try:
            return reverse(name)
        except Exception:
            return default_url

    categories = [
        {
            'key': 'news',
            'title': '📰 समाचार',
            'english_name': 'News Articles',
            'submit_url': try_reverse('news:news_create'),
            'submit_text': '+ समाचार भेजें',
            'empty_text': 'आपने अभी तक कोई समाचार नहीं भेजा है।',
            'items': news_items,
            'count': len(news_items),
        },
        {
            'key': 'stories',
            'title': '📖 कहानी',
            'english_name': 'Stories',
            'submit_url': try_reverse('storytelling:create_story'),
            'submit_text': '+ कहानी भेजें',
            'empty_text': 'आपने अभी तक कोई कहानी नहीं भेजी है।',
            'items': story_items,
            'count': len(story_items),
        },
        {
            'key': 'rentals',
            'title': '🏠 किरायाक घर',
            'english_name': 'PG & Rental Listings',
            'submit_url': try_reverse('pg_rental:add_listing'),
            'submit_text': '+ लिस्टिंग जोड़ें',
            'empty_text': 'आपने अभी तक कोई PG/किराया लिस्टिंग नहीं भेजी है।',
            'items': rental_items,
            'count': len(rental_items),
        },
        {
            'key': 'jobs',
            'title': '💼 रोजगार',
            'english_name': 'Job Posts',
            'submit_url': try_reverse('job_portal:create_job'),
            'submit_text': '+ नौकरी जोड़ें',
            'empty_text': 'आपने अभी तक कोई नौकरी नहीं भेजी है।',
            'items': job_items,
            'count': len(job_items),
        },
        {
            'key': 'lost_found',
            'title': '🔍 हरायल आ भेटल वस्तु',
            'english_name': 'Lost & Found Items',
            'submit_url': try_reverse('lost_and_found:create_item'),
            'submit_text': '+ वस्तु पोस्ट करें',
            'empty_text': 'आपने अभी तक कोई हरायल/भेटल वस्तु नहीं भेजी है।',
            'items': lost_items,
            'count': len(lost_items),
        },
        {
            'key': 'events',
            'title': '🎉 पावन पर्व एवं आयोजन',
            'english_name': 'Events & Festivals',
            'submit_url': try_reverse('events:event_submit'),
            'submit_text': '+ आयोजन भेजें',
            'empty_text': 'आपने अभी तक कोई आयोजन नहीं भेजा है।',
            'items': event_items,
            'count': len(event_items),
        },
        {
            'key': 'pride',
            'title': '👨‍🎓 मिथिला गौरव एवं विद्वान',
            'english_name': 'Mithila Pride & Scholars',
            'submit_url': try_reverse('mithila_pride:person_submit'),
            'submit_text': '+ विद्वान profile भेजें',
            'empty_text': 'आपने अभी तक कोई विद्वान profile नहीं भेजी है।',
            'items': pride_items,
            'count': len(pride_items),
        },
        {
            'key': 'pandits',
            'title': '🧑‍🦳 पंडित एवं ज्योतिषी',
            'english_name': 'Pandits & Astrologers',
            'submit_url': try_reverse('pandits:profile_onboard'),
            'submit_text': '+ पंडित profile जोड़ें',
            'empty_text': 'आपने अभी तक कोई पंडित profile नहीं बनाई है।',
            'items': pandit_items,
            'count': len(pandit_items),
        },
        {
            'key': 'cab_auto',
            'title': '🚕 कैब एवं ऑटो',
            'english_name': 'Cab & Auto Drivers',
            'submit_url': try_reverse('cab_auto:driver_register'),
            'submit_text': '+ चालक profile जोड़ें',
            'empty_text': 'आपने अभी तक कोई चालक profile नहीं बनाई है।',
            'items': driver_items,
            'count': len(driver_items),
        },
        {
            'key': 'ghatkaiti',
            'title': '👥 घटकैती',
            'english_name': 'Ghatkaiti Matrimonial',
            'submit_url': try_reverse('ghatkaiti:profile_create'),
            'submit_text': '+ वैवाहिक profile जोड़ें',
            'empty_text': 'आपने अभी तक कोई वैवाहिक profile नहीं बनाई है।',
            'items': mat_items,
            'count': len(mat_items),
        },
        {
            'key': 'parichay',
            'title': '📍 मिथिला परिचय',
            'english_name': 'Mithila Parichay / Wiki',
            'submit_url': try_reverse('delhi_wiki:area_list'),
            'submit_text': '+ स्थान/Landmark जोड़ें',
            'empty_text': 'आपने अभी तक कोई स्थान/Landmark नहीं जोड़ा है।',
            'items': parichay_items,
            'count': len(parichay_items),
        },
        {
            'key': 'subreddits',
            'title': '👥 Community Requests',
            'english_name': 'Subreddits Created',
            'submit_url': try_reverse('subreddits:create'),
            'submit_text': '+ समुदाय बनाएँ',
            'empty_text': 'आपने अभी तक कोई समुदाय नहीं बनाया है।',
            'items': subreddit_items,
            'count': len(subreddit_items),
        },
        {
            'key': 'posts',
            'title': '📝 Community Posts',
            'english_name': 'User Posts',
            'submit_url': try_reverse('posts:create'),
            'submit_text': '+ पोस्ट बनाएँ',
            'empty_text': 'आपने अभी तक कोई पोस्ट नहीं की है।',
            'items': post_items,
            'count': len(post_items),
        },
    ]

    all_flat_items = [item for c in categories for item in c['items']]
    total_submissions = sum(c['count'] for c in categories)
    pending_count = sum(1 for item in all_flat_items if item['status'] == 'PENDING')
    approved_count = sum(1 for item in all_flat_items if item['status'] == 'APPROVED')
    rejected_count = sum(1 for item in all_flat_items if item['status'] == 'REJECTED')
    needs_changes_count = sum(1 for item in all_flat_items if item['status'] == 'NEEDS_CHANGES')

    context = {
        'categories': categories,
        'all_flat_items': all_flat_items,
        'total_submissions': total_submissions,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'needs_changes_count': needs_changes_count,
    }
    return render(request, 'core/user_submissions.html', context)

