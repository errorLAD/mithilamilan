from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
import datetime

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('festival', 'Festival'),
        ('cultural', 'Cultural'),
        ('religious', 'Religious'),
        ('community', 'Community'),
        ('educational', 'Educational'),
        ('local', 'Local Event'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=285, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='festival')
    cover_image = models.ImageField(upload_to='events/covers/', null=True, blank=True)
    short_description = models.TextField(help_text="Brief summary shown on listing cards")
    about = models.TextField(help_text="Full detailed description of the event")
    history_background = models.TextField(blank=True, help_text="Historical or cultural significance")
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    location = models.CharField(max_length=255, help_text="e.g. Darbhanga, Bihar")
    venue_info = models.TextField(blank=True, help_text="Specific venue address or hall details")
    organizer = models.CharField(max_length=255, blank=True, help_text="Organizer or Samiti name")
    contact_info = models.CharField(max_length=255, blank=True, help_text="Phone number or contact details")
    map_location = models.CharField(max_length=500, blank=True, help_text="Google Maps URL or embed query")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submitted_events'
    )
    submitter_name = models.CharField(max_length=150, blank=True)
    submitter_email = models.EmailField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', '-is_featured', 'title']
        verbose_name = 'Event & Festival'
        verbose_name_plural = 'Events & Festivals'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'event'
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={'slug': self.slug})

    @property
    def is_multi_day(self):
        return self.end_date > self.start_date

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def timing_status(self):
        today = timezone.localdate()
        if today < self.start_date:
            return 'Upcoming'
        elif self.start_date <= today <= self.end_date:
            return 'Ongoing'
        else:
            return 'Completed'

class EventScheduleDay(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedule_days')
    day_number = models.IntegerField(default=1)
    date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=255, help_text="e.g. Day 1 — 10 October / Maha Saptami")
    morning_program = models.TextField(blank=True)
    afternoon_program = models.TextField(blank=True)
    evening_program = models.TextField(blank=True)

    class Meta:
        ordering = ['day_number', 'date']

    def __str__(self):
        return f"{self.event.title} - Day {self.day_number}"

class EventImportantDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='important_dates')
    title = models.CharField(max_length=255, help_text="e.g. Sandhi Puja Timings")
    date_info = models.CharField(max_length=255, help_text="e.g. 13 Oct, 11:45 PM - 12:33 AM")
    details = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.event.title} - {self.title}"

class EventGallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Gallery Image for {self.event.title}"
