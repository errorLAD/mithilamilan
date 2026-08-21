from django.db import models
from django.conf import settings
from django.utils import timezone

class News(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    CATEGORY_CHOICES = [
        ('MITHILA', 'मिथिला'),
        ('BIHAR', 'बिहार'),
        ('EDUCATION', 'शिक्षा'),
        ('JOBS', 'रोजगार'),
        ('SOCIETY', 'समाज'),
        ('CULTURE', 'संस्कृति'),
        ('POLITICS', 'राजनीति'),
        ('BUSINESS', 'व्यापार'),
        ('SPORTS', 'खेल'),
        ('TECH', 'तकनीक'),
        ('LOCAL', 'स्थानीय समाचार'),
    ]

    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=500, blank=True, help_text="Short article summary")
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='LOCAL')
    location = models.CharField(max_length=100, blank=True)
    source_name = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_news')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])