from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import models
from .models import Story
from .forms import StoryForm

def is_superuser(user):
    return user.is_superuser

def story_list(request):
    stories_qs = Story.objects.filter(status='APPROVED').order_by('-created_at')
    
    # Category filter
    category = request.GET.get('category', '').strip()
    if category:
        stories_qs = stories_qs.filter(category=category)

    # Search filter
    query = request.GET.get('q', '').strip()
    if query:
        stories_qs = stories_qs.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(excerpt__icontains=query) |
            models.Q(location__icontains=query) |
            models.Q(author__username__icontains=query)
        )
    
    featured_story = stories_qs.first()
    other_stories = stories_qs[1:] if featured_story else []

    paginator = Paginator(other_stories, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'storytelling/story_list.html', {
        'featured_story': featured_story,
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'categories': Story.CATEGORY_CHOICES,
    })

@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.status = 'PENDING'
            story.save()
            messages.success(request, 'आपकी कहानी समीक्षा के लिए भेज दी गई है। एडमिन अनुमोदन के बाद यह प्रकाशित होगी।')
            return redirect('core:user_submissions')
        else:
            messages.error(request, 'कृपया सभी आवश्यक फ़ील्ड सही तरीके से भरें।')
    else:
        form = StoryForm()
    return render(request, 'storytelling/create_story.html', {'form': form, 'categories': Story.CATEGORY_CHOICES})

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.status != 'APPROVED' and not (request.user.is_staff or request.user == story.author):
        messages.warning(request, 'यह कहानी अभी समीक्षा में है और केवल आपको दिखाई दे रही है।')
    
    story.views += 1
    story.save(update_fields=['views'])

    related_stories = Story.objects.filter(status='APPROVED', category=story.category).exclude(pk=story.pk)[:3]

    return render(request, 'storytelling/story_detail.html', {
        'story': story,
        'related_stories': related_stories,
    })

@login_required
@user_passes_test(is_superuser)
def pending_stories(request):
    stories = Story.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'storytelling/pending_stories.html', {'stories': stories})

@login_required
@user_passes_test(is_superuser)
def approve_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    story.approve(request.user)
    messages.success(request, f'Story "{story.title}" has been approved.')
    return redirect('storytelling:pending_stories')

@login_required
@user_passes_test(is_superuser)
def reject_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    reason = request.POST.get('reason', '')
    story.reject(request.user, reason)
    messages.success(request, f'Story "{story.title}" has been rejected.')
    return redirect('storytelling:pending_stories')

@login_required
def my_stories(request):
    stories = Story.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'storytelling/my_stories.html', {'stories': stories})

@login_required
def like_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.user in story.likes.all():
        story.likes.remove(request.user)
        action = 'unliked'
    else:
        story.likes.add(request.user)
        action = 'liked'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'likes_count': story.likes.count()
        })
    
    return redirect('storytelling:story_detail', pk=pk)
