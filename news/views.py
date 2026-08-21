from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import News

def news_list(request):
    # Only show APPROVED news to public
    news_qs = News.objects.filter(status='APPROVED').order_by('-created_at')
    
    # Category filter
    category = request.GET.get('category', '').strip()
    if category:
        news_qs = news_qs.filter(category=category)

    # Search filter
    query = request.GET.get('q', '').strip()
    if query:
        news_qs = news_qs.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(summary__icontains=query) |
            models.Q(location__icontains=query)
        )

    # Featured Story (first item in results)
    featured_news = news_qs.first()
    other_news = news_qs[1:] if featured_news else []

    # Pagination for news feed
    paginator = Paginator(other_news, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Sidebar Trending News
    trending_news = News.objects.filter(status='APPROVED').order_by('-views')[:5]

    return render(request, 'news/news_list.html', {
        'featured_news': featured_news,
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'trending_news': trending_news,
        'categories': News.CATEGORY_CHOICES,
    })

def news_detail(request, pk):
    # Show news if approved or if author/staff is viewing
    news = get_object_or_404(News, pk=pk)
    if news.status != 'APPROVED' and not (request.user.is_authenticated and (request.user.is_staff or request.user == news.author)):
        messages.warning(request, "यह समाचार अभी समीक्षा में है और केवल आपको दिखाई दे रहा है।")
    
    news.increment_views()
    related_news = News.objects.filter(status='APPROVED', category=news.category).exclude(pk=news.pk)[:3]

    return render(request, 'news/news_detail.html', {
        'news': news,
        'related_news': related_news,
    })

@login_required
def news_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        summary = request.POST.get('summary', '').strip()
        category = request.POST.get('category', 'LOCAL')
        content = request.POST.get('content', '').strip()
        location = request.POST.get('location', '').strip()
        source_name = request.POST.get('source_name', '').strip()
        source_url = request.POST.get('source_url', '').strip()
        image = request.FILES.get('image')

        if title and content:
            news = News.objects.create(
                title=title,
                summary=summary,
                category=category,
                content=content,
                location=location,
                source_name=source_name,
                source_url=source_url,
                image=image,
                author=request.user,
                status='PENDING'
            )
            messages.success(request, "आपका समाचार समीक्षा के लिए भेज दिया गया है। एडमिन अनुमोदन के बाद यह लाइव होगा।")
            return redirect('core:user_submissions')
        else:
            messages.error(request, "कृपया शीर्षक एवं मुख्य समाचार भरें।")

    return render(request, 'news/news_create.html', {
        'categories': News.CATEGORY_CHOICES,
    })