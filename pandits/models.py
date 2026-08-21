from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import re

class PanditProfile(models.Model):
    PROFILE_TYPE_CHOICES = [
        ('pandit', 'Pandit'),
        ('astrologer', 'Astrologer'),
        ('both', 'Pandit & Astrologer'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pandit_profiles'
    )
    
    full_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES, default='pandit')
    profile_photo = models.ImageField(upload_to='pandits/profiles/', null=True, blank=True)
    designation = models.CharField(max_length=255, help_text="e.g. Senior Vedic Scholar & Karma Kanda Specialist")
    
    whatsapp_number = models.CharField(max_length=20, help_text="Mandatory. Include country code if outside India e.g. 9876543210")
    phone_number = models.CharField(max_length=20, blank=True)
    
    location = models.CharField(max_length=255, help_text="e.g. Darbhanga, Bihar")
    address_area = models.TextField(blank=True, help_text="Local area or full address details")
    
    experience_years = models.IntegerField(default=5, help_text="Years of experience")
    languages = models.CharField(max_length=255, help_text="e.g. Maithili, Hindi, Sanskrit, English")
    specialization = models.CharField(max_length=255, help_text="e.g. Griha Pravesh, Vivah, Kundali Reading, Vastu")
    services_offered = models.TextField(help_text="Detailed list or bullet points of rituals, pujas or horoscopes offered")
    about = models.TextField(help_text="Professional summary and background")
    availability = models.CharField(max_length=255, default="Mon - Sun: 8:00 AM - 8:00 PM")
    service_pricing = models.TextField(blank=True, help_text="Optional pricing details e.g. Kundali Reading: ₹501")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False, help_text="Shows Verified Badge on profile")
    is_featured = models.BooleanField(default=False)
    
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-is_verified', '-experience_years', 'full_name']
        verbose_name = 'Pandit & Astrologer Profile'
        verbose_name_plural = 'Pandit & Astrologer Profiles'

    def __str__(self):
        return f"{self.full_name} ({self.get_profile_type_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            prefix = 'astrologer' if self.profile_type == 'astrologer' else 'pandit'
            base_slug = slugify(f"{prefix}-{self.full_name}") or 'profile'
            slug = base_slug
            counter = 1
            while PanditProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
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
            prefilled_text = f"Namaste {self.full_name} ji, I found your profile on Mithila Platform and would like to inquire about your services."
        from urllib.parse import quote
        return f"https://wa.me/{num}?text={quote(prefilled_text)}"

    def get_absolute_url(self):
        if self.profile_type == 'astrologer':
            return reverse('pandits:astrologer_detail', kwargs={'slug': self.slug})
        return reverse('pandits:pandit_detail', kwargs={'slug': self.slug})

class PanditGallery(models.Model):
    profile = models.ForeignKey(PanditProfile, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='pandits/gallery/')
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Gallery for {self.profile.full_name}"

class ConsultationRequest(models.Model):
    LOCATION_CHOICES = [
        ('offline', 'In-Person / At Home'),
        ('online', 'Online / Video Consultation'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Response'),
        ('contacted', 'Contacted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    profile = models.ForeignKey(PanditProfile, on_delete=models.CASCADE, related_name='consultation_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=150)
    user_phone = models.CharField(max_length=20)
    user_whatsapp = models.CharField(max_length=20, blank=True)
    service_required = models.CharField(max_length=255)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=100, blank=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='offline')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request for {self.profile.full_name} from {self.user_name}"
