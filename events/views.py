from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Event, EventScheduleDay, EventImportantDate, EventGallery
from .forms import EventSubmissionForm

def event_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    location = request.GET.get('location', '').strip()
    timing_status = request.GET.get('timing', '').strip()
    sort_by = request.GET.get('sort', 'date_asc').strip()

    events_qs = Event.objects.filter(status__in=['approved', 'published'])

    if query:
        events_qs = events_qs.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(about__icontains=query) |
            Q(location__icontains=query) |
            Q(organizer__icontains=query)
        )

    if category:
        events_qs = events_qs.filter(category=category)

    if location:
        events_qs = events_qs.filter(location__icontains=location)

    today = timezone.localdate()
    if timing_status == 'upcoming':
        events_qs = events_qs.filter(start_date__gt=today)
    elif timing_status == 'ongoing':
        events_qs = events_qs.filter(start_date__lte=today, end_date__gte=today)
    elif timing_status == 'completed':
        events_qs = events_qs.filter(end_date__lt=today)

    if sort_by == 'date_desc':
        events_qs = events_qs.order_by('-start_date', 'title')
    elif sort_by == 'title':
        events_qs = events_qs.order_by('title')
    else:  # default date_asc
        events_qs = events_qs.order_by('start_date', '-is_featured')

    featured_events = Event.objects.filter(status__in=['approved', 'published'], is_featured=True)[:3]
    
    paginator = Paginator(events_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Event.CATEGORY_CHOICES

    context = {
        'events': page_obj,
        'page_obj': page_obj,
        'featured_events': featured_events,
        'query': query,
        'category': category,
        'location': location,
        'timing_status': timing_status,
        'sort_by': sort_by,
        'categories': categories,
        'total_count': events_qs.count(),
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    # Check permissions if not published/approved
    if event.status not in ['approved', 'published']:
        if not (request.user.is_authenticated and (request.user.is_staff or request.user == event.submitted_by)):
            messages.warning(request, "This event is currently under admin review.")
            return redirect('events:event_list')

    # Multi-day schedule
    schedule_days = event.schedule_days.all().order_by('day_number')
    important_dates = event.important_dates.all()
    gallery = event.gallery_images.all()

    # Nearby / Related events: events around the same location or within +-15 days of start_date
    start_window = event.start_date - timedelta(days=15)
    end_window = event.start_date + timedelta(days=15)
    
    related_events = Event.objects.filter(
        status__in=['approved', 'published']
    ).exclude(pk=event.pk).filter(
        Q(location__icontains=event.location.split(',')[0]) |
        Q(start_date__gte=start_window, start_date__lte=end_window) |
        Q(category=event.category)
    ).distinct()[:4]

    context = {
        'event': event,
        'schedule_days': schedule_days,
        'important_dates': important_dates,
        'gallery': gallery,
        'related_events': related_events,
    }
    return render(request, 'events/event_detail.html', context)

def event_submit(request):
    if request.method == 'POST':
        form = EventSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            if request.user.is_authenticated:
                event.submitted_by = request.user
                if not event.submitter_name:
                    event.submitter_name = request.user.get_full_name() or request.user.username
                if not event.submitter_email:
                    event.submitter_email = request.user.email

            # Admin submissions publish directly
            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                event.status = 'published'
                messages.success(request, f"Event '{event.title}' published directly!")
            else:
                event.status = 'pending'
                messages.success(request, f"Thank you! '{event.title}' submitted successfully. It will appear publicly after Admin approval.")
            
            event.save()

            # Process optional multi-day schedule entries from POST request
            day_titles = request.POST.getlist('schedule_day_title[]')
            morning_progs = request.POST.getlist('schedule_morning[]')
            afternoon_progs = request.POST.getlist('schedule_afternoon[]')
            evening_progs = request.POST.getlist('schedule_evening[]')
            
            for idx, title in enumerate(day_titles):
                if title.strip():
                    EventScheduleDay.objects.create(
                        event=event,
                        day_number=idx + 1,
                        title=title.strip(),
                        morning_program=morning_progs[idx] if idx < len(morning_progs) else '',
                        afternoon_program=afternoon_progs[idx] if idx < len(afternoon_progs) else '',
                        evening_program=evening_progs[idx] if idx < len(evening_progs) else '',
                    )

            return redirect(event.get_absolute_url() if event.status in ['approved', 'published'] else 'events:event_list')
    else:
        form = EventSubmissionForm()

    return render(request, 'events/event_form.html', {'form': form})

def event_ics_export(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    start_str = event.start_date.strftime('%Y%m%d')
    end_str = (event.end_date + timedelta(days=1)).strftime('%Y%m%d')
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Ok Delhi Mithila Platform//Event Calendar//EN
BEGIN:VEVENT
SUMMARY:{event.title}
DESCRIPTION:{event.short_description}
LOCATION:{event.location}
DTSTART;VALUE=DATE:{start_str}
DTEND;VALUE=DATE:{end_str}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""

    response = HttpResponse(ics_content, content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="{event.slug}.ics"'
    return response
