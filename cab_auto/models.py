from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import re

class DriverProfile(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('auto', 'Auto / E-Rickshaw'),
        ('taxi', 'Taxi / Cab'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
        ('published', 'Published'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver_profiles')
    full_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    photo = models.ImageField(upload_to='cab_auto/drivers/', null=True, blank=True)
    age = models.IntegerField(default=30)
    
    mobile_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, help_text="Mandatory WhatsApp number")
    
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='auto')
    vehicle_model = models.CharField(max_length=150, help_text="e.g. Bajaj RE Maxima / Swift Dzire AC")
    vehicle_number = models.CharField(max_length=50, blank=True, help_text="Registration Number (Optional)")
    
    service_area = models.CharField(max_length=255, help_text="e.g. Darbhanga Railway Station, Airport, Madhubani Local")
    experience_years = models.IntegerField(default=5)
    available_hours = models.CharField(max_length=150, default="24/7 Available")
    about = models.TextField(blank=True, help_text="Short background or routes covered")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-is_verified', 'full_name']
        verbose_name = 'Cab & Auto Driver Profile'
        verbose_name_plural = 'Cab & Auto Driver Profiles'

    def __str__(self):
        return f"{self.full_name} ({self.get_vehicle_type_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.vehicle_type}-{self.full_name}") or 'driver'
            slug = base_slug
            counter = 1
            while DriverProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def clean_whatsapp_number(self):
        cleaned = re.sub(r'[^\d]', '', self.whatsapp_number or '')
        if len(cleaned) == 10:
            cleaned = '91' + cleaned
        return cleaned

    def get_whatsapp_url(self, prefilled_text=None):
        num = self.clean_whatsapp_number
        if not prefilled_text:
            prefilled_text = f"Hello {self.full_name} ji, I found your {self.get_vehicle_type_display()} listing on Mithila Platform and would like to inquire about ride booking."
        from urllib.parse import quote
        return f"https://wa.me/{num}?text={quote(prefilled_text)}"

    def get_absolute_url(self):
        return reverse('cab_auto:driver_detail', kwargs={'slug': self.slug})
