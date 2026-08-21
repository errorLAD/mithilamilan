from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import re

class MatrimonialProfile(models.Model):
    LOOKING_FOR_CHOICES = [
        ('son', 'Suitable Match for Son'),
        ('daughter', 'Suitable Match for Daughter'),
        ('other', 'Suitable Match for Relative'),
    ]

    GENDER_CHOICES = [
        ('male', 'Groom / Male'),
        ('female', 'Bride / Female'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='matrimonial_profiles')
    
    looking_for = models.CharField(max_length=20, choices=LOOKING_FOR_CHOICES, default='son')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    full_name = models.CharField(max_length=150, help_text="Candidate Name")
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    
    age = models.IntegerField(default=25)
    height = models.CharField(max_length=50, blank=True, help_text="e.g. 5' 8\" (Optional)")
    
    education = models.CharField(max_length=255, help_text="e.g. B.Tech (IIT), MBA / M.A. Sanskrit")
    profession = models.CharField(max_length=255, help_text="e.g. Senior Software Engineer at MNC / Govt Officer")
    
    location = models.CharField(max_length=255, help_text="e.g. Delhi NCR")
    native_place = models.CharField(max_length=255, help_text="e.g. Madhubani / Darbhanga, Bihar")
    current_city = models.CharField(max_length=255, help_text="e.g. Noida / New Delhi / Bangalore")
    
    community_family_details = models.TextField(blank=True, help_text="Family lineage or gotra background (Optional)")
    about_person = models.TextField(help_text="Overview of personality, hobbies, background")
    family_info = models.TextField(help_text="Father's profession, mother, siblings, background")
    expectations = models.TextField(help_text="Partner preferences and family expectations")
    
    contact_person_name = models.CharField(max_length=150, help_text="Parent or guardian name")
    whatsapp_number = models.CharField(max_length=20, help_text="Mandatory WhatsApp number for private contact button")
    profile_photo = models.ImageField(upload_to='ghatkaiti/photos/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = 'Ghatkaiti Matrimonial Profile'
        verbose_name_plural = 'Ghatkaiti Matrimonial Profiles'

    def __str__(self):
        return f"{self.get_looking_for_display()} - {self.full_name} ({self.age} Yrs)"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.gender}-{self.full_name}") or 'matrimonial'
            slug = base_slug
            counter = 1
            while MatrimonialProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
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
            prefilled_text = f"Namaste {self.contact_person_name} ji, I saw your matrimonial profile post for {self.full_name} on Ghatkaiti Mithila Platform and would like to connect."
        from urllib.parse import quote
        return f"https://wa.me/{num}?text={quote(prefilled_text)}"

    def get_absolute_url(self):
        return reverse('ghatkaiti:profile_detail', kwargs={'slug': self.slug})

class ProfileReport(models.Model):
    REASON_CHOICES = [
        ('misleading', 'Misleading Information'),
        ('fake_profile', 'Fake Profile'),
        ('inappropriate', 'Inappropriate Content'),
        ('other', 'Other Reason'),
    ]

    profile = models.ForeignKey(MatrimonialProfile, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reporter_name = models.CharField(max_length=150, blank=True)
    reporter_email = models.EmailField(blank=True)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, default='misleading')
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.profile.full_name} ({self.reason})"
