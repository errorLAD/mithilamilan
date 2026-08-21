from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import Subreddit
from .forms import SubredditCreateForm, SubredditUpdateForm
from users.models import CustomUser
from posts.models import Post

def is_superadmin(user):
    return user.is_superuser

def subreddit_list(request):
    if request.user.is_superuser:
        subreddits = Subreddit.objects.all()
    else:
        subreddits = Subreddit.objects.filter(approval_status='approved')
    return render(request, 'subreddits/list.html', {'subreddits': subreddits})

@login_required
def subreddit_create(request):
    if request.method == 'POST':
        form = SubredditCreateForm(request.POST, request.FILES)
        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.creator = request.user
            subreddit.save()
            # Add the creator as a moderator
            subreddit.moderators.add(request.user)
            messages.success(request, 'Subreddit created successfully! It will be visible after admin approval.')
            return redirect('subreddits:subreddit_detail', slug=subreddit.slug)
    else:
        form = SubredditCreateForm()
    return render(request, 'subreddits/create.html', {'form': form})

@login_required
def subreddit_detail(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if not subreddit.is_approved() and not request.user.is_superuser:
        messages.error(request, 'This subreddit is pending approval.')
        return redirect('core:home')
    context = {
        'subreddit': subreddit,
        'is_subscribed': request.user.is_authenticated and subreddit.subscribers.filter(id=request.user.id).exists(),
        'subscriber_count': subreddit.get_member_count(),
        'is_moderator': request.user.is_authenticated and subreddit.moderators.filter(id=request.user.id).exists()
    }
    return render(request, 'subreddits/detail.html', context)

@login_required
def subreddit_edit(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if request.user not in subreddit.moderators.all():
        messages.error(request, 'You do not have permission to edit this subreddit.')
        return redirect('subreddits:subreddit_detail', slug=slug)
    
    if request.method == 'POST':
        form = SubredditUpdateForm(request.POST, request.FILES, instance=subreddit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subreddit updated successfully!')
            return redirect('subreddits:subreddit_detail', slug=slug)
    else:
        form = SubredditUpdateForm(instance=subreddit)
    return render(request, 'subreddits/edit.html', {'form': form, 'subreddit': subreddit})

@login_required
@user_passes_test(is_superadmin)
def subreddit_approval_list(request):
    pending_subreddits = Subreddit.objects.filter(approval_status='pending')
    return render(request, 'subreddits/approval_list.html', {
        'pending_subreddits': pending_subreddits
    })

@login_required
@user_passes_test(is_superadmin)
def approve_subreddit(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if request.method == 'POST':
        subreddit.approval_status = 'approved'
        subreddit.approved_by = request.user
        subreddit.approved_at = timezone.now()
        subreddit.save()
        messages.success(request, f'Subreddit "{subreddit.name}" has been approved.')
    return redirect('subreddits:approval_list')

@login_required
@user_passes_test(is_superadmin)
def reject_subreddit(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if request.method == 'POST':
        subreddit.approval_status = 'rejected'
        subreddit.approved_by = request.user
        subreddit.approved_at = timezone.now()
        subreddit.save()
        messages.warning(request, f'Subreddit "{subreddit.name}" has been rejected.')
    return redirect('subreddits:approval_list')

@login_required
def subscribe(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if subreddit.is_pending():
        messages.warning(request, 'Cannot subscribe to a pending subreddit.')
        return redirect('core:home')
    subreddit.subscribers.add(request.user)
    messages.success(request, f'Successfully subscribed to r/{subreddit.name}')
    return redirect('core:home')

@login_required
def unsubscribe(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    subreddit.subscribers.remove(request.user)
    messages.success(request, f'Successfully unsubscribed from r/{subreddit.name}')
    return redirect('core:home')

def search(request):
    query = request.GET.get('q', '').strip()
    filter_type = request.GET.get('type', 'all')
    sort_by = request.GET.get('sort', 'relevance')

    if not query:
        return redirect('core:home')
    
    # Search subreddits
    subreddits = Subreddit.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query),
        approval_status='approved'
    ).annotate(member_count=Count('subscribers'))

    # Search posts
    posts = Post.objects.filter(
        Q(title__icontains=query) | 
        Q(content__icontains=query),
        subreddit__approval_status='approved'
    ).select_related('author', 'subreddit').prefetch_related('comments', 'upvotes', 'downvotes')
    
    if sort_by == 'newest':
        posts = posts.order_by('-created_at')
    elif sort_by == 'top':
        posts = posts.order_by('-score', '-created_at')

    posts_count = posts.count()
    subreddits_count = subreddits.count()
    total_results = posts_count + subreddits_count

    user_votes = {}
    subscribed_subreddit_ids = []
    if request.user.is_authenticated:
        for p in posts:
            if p.upvotes.filter(id=request.user.id).exists():
                user_votes[p.slug] = 'up'
            elif p.downvotes.filter(id=request.user.id).exists():
                user_votes[p.slug] = 'down'
            else:
                user_votes[p.slug] = 'none'
        subscribed_subreddit_ids = list(Subreddit.objects.filter(subscribers=request.user).values_list('id', flat=True))
    
    # Popular subreddits for sidebar
    popular_subreddits = Subreddit.objects.filter(
        approval_status='approved'
    ).annotate(member_count=Count('subscribers')).order_by('-member_count')[:5]
    
    context = {
        'query': query,
        'filter_type': filter_type,
        'sort_by': sort_by,
        'subreddits': subreddits,
        'posts': posts,
        'posts_count': posts_count,
        'subreddits_count': subreddits_count,
        'total_results': total_results,
        'popular_subreddits': popular_subreddits,
        'user_votes': user_votes,
        'subscribed_subreddit_ids': subscribed_subreddit_ids,
    }
    return render(request, 'subreddits/search.html', context) 