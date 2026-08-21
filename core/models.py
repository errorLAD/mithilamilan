from django.db import models
from django.conf import settings
from django.utils.text import slugify

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    is_popular = models.BooleanField(default=False)
    icon = models.CharField(max_length=50, default='📍', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.name}, {self.state.code or self.state.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Locality(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='localities')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Localities'
        unique_together = ('city', 'slug')

    def __str__(self):
        return f"{self.name}, {self.city.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class UserLocationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location_preference')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.city.name if self.city else 'All India'}"

class AdminActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_activities')
    action = models.CharField(max_length=150)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Admin Activity Log'
        verbose_name_plural = 'Admin Activity Logs'

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.action} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

class PlatformSetting(models.Model):
    site_name = models.CharField(max_length=150, default="MithilaMilan")
    site_tagline = models.CharField(max_length=255, default="जय मिथिला! जय मैथिली!")
    support_email = models.EmailField(default="support@mithilamilan.com")
    contact_phone = models.CharField(max_length=20, default="+91 9876543210")
    maintenance_mode = models.BooleanField(default=False)
    allow_registrations = models.BooleanField(default=True)
    require_submission_approval = models.BooleanField(default=True)
    
    featured_community_slugs = models.TextField(blank=True, help_text="Comma-separated community slugs for homepage")
    featured_news_ids = models.TextField(blank=True, help_text="Comma-separated news IDs")
    featured_event_ids = models.TextField(blank=True, help_text="Comma-separated event IDs")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.site_name} Configuration"

class SEOPageMeta(models.Model):
    path = models.CharField(max_length=255, unique=True, help_text="e.g. / or /news/ or /r/madhubani/")
    seo_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    focus_keyword = models.CharField(max_length=150, blank=True)
    secondary_keywords = models.CharField(max_length=255, blank=True)
    canonical_url = models.URLField(blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.CharField(max_length=500, blank=True)
    robots_index = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)
    schema_type = models.CharField(max_length=50, default='Article')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['path']
        verbose_name = 'SEO Page Meta'
        verbose_name_plural = 'SEO Page Metas'

    def __str__(self):
        return f"{self.path} - {self.seo_title or 'No Title'}"

class RobotsConfig(models.Model):
    content = models.TextField(default="User-agent: *\nDisallow: /admin/\nDisallow: /admin-panel/\nDisallow: /users/login/\nDisallow: /users/signup/\n\nSitemap: https://mithilamilan.com/sitemap.xml")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "robots.txt Configuration"

class MarketingCampaign(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Active', 'Active'),
        ('Paused', 'Paused'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    platform = models.CharField(max_length=100, default='Google Ads')
    start_date = models.DateField()
    end_date = models.DateField()
    target_audience = models.CharField(max_length=255, blank=True)
    landing_page = models.CharField(max_length=255, default='/')
    utm_source = models.CharField(max_length=100, default='google')
    utm_medium = models.CharField(max_length=100, default='cpc')
    utm_campaign = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.platform})"

class SocialAccountTrack(models.Model):
    platform = models.CharField(max_length=50) # Facebook, Instagram, YouTube, WhatsApp, X
    handle_or_name = models.CharField(max_length=150)
    url = models.URLField()
    followers = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.platform} - {self.handle_or_name}"

class SEOIntegrationSetting(models.Model):
    gsc_property_id = models.CharField(max_length=255, blank=True, help_text="Google Search Console Domain Property")
    gsc_connected = models.BooleanField(default=False)
    ga4_measurement_id = models.CharField(max_length=100, blank=True, help_text="e.g. G-XXXXXXXXXX")
    ga4_connected = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "SEO & Digital Marketing API Integrations"


class FooterSetting(models.Model):
    site_name = models.CharField(max_length=100, default="MithilaMilan")
    tagline = models.CharField(max_length=255, default="मिथिला के लोक, संस्कृति आ समाज के एक डिजिटल मंच।")
    short_description = models.TextField(
        default="MithilaMilan is a community platform created to connect people, culture, businesses, stories, opportunities and information related to Mithila."
    )
    subline = models.CharField(max_length=100, default="Made with ❤️ in Mithila")
    contact_email = models.EmailField(default="contact@mithilamilan.com")
    support_email = models.EmailField(default="support@mithilamilan.com")
    report_issue_email = models.EmailField(default="safety@mithilamilan.com")
    
    # Social Links
    facebook_url = models.URLField(blank=True, default="https://facebook.com/mithilamilan")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/mithilamilan")
    youtube_url = models.URLField(blank=True, default="https://youtube.com/@mithilamilan")
    x_twitter_url = models.URLField(blank=True, default="https://x.com/mithilamilan")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/company/mithilamilan")
    
    # Copyright & Disclaimers
    copyright_text = models.CharField(max_length=255, default="© 2026 MithilaMilan. All rights reserved.")
    platform_disclaimer = models.TextField(
        default="Important: MithilaMilan is a community and information platform. Content, listings, advertisements, products, services, events, jobs, rentals and other information may be submitted or provided by users, businesses, organizers or third parties. MithilaMilan does not automatically endorse or guarantee every third-party listing or claim.\n\nMithilaMilan is not responsible for fraudulent, misleading, unauthorized or unlawful activities carried out by third parties through information, listings, posts, advertisements, transactions or communications on the platform, subject to applicable law.\n\nUsers are responsible for verifying information, identities, offers, prices, payment details and other claims before entering into any transaction or agreement."
    )
    fraud_warning_title = models.CharField(max_length=100, default="⚠️ Stay Safe")
    fraud_warning_text = models.TextField(
        default="Never share your OTP, password, PIN, card details or other sensitive information with anyone claiming to represent MithilaMilan.\n\nMithilaMilan will never ask you to transfer money to a personal account for verification or account activation.\n\nIf you notice suspicious activity, report it to us through the platform."
    )
    user_content_disclaimer = models.TextField(
        default="User-generated content belongs to its respective authors. Users are responsible for the content they submit. MithilaMilan may review, moderate, restrict or remove content that violates applicable laws, platform policies or community guidelines."
    )
    marketplace_disclaimer = models.TextField(
        default="Products and services listed by independent sellers or providers may be subject to separate seller terms, availability, pricing, delivery and return conditions. Users should review the applicable details before purchasing."
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Footer & Platform Settings'
        verbose_name_plural = 'Footer & Platform Settings'

    def __str__(self):
        return f"Footer Settings - {self.site_name}"


class LegalPage(models.Model):
    SLUG_CHOICES = [
        ('terms', 'Terms of Service'),
        ('privacy', 'Privacy Policy'),
        ('cancellation', 'Cancellation Policy'),
        ('community-guidelines', 'Community Guidelines'),
        ('content-policy', 'Content Policy'),
        ('refund-policy', 'Refund Policy'),
        ('disclaimer', 'Disclaimer'),
    ]

    slug = models.SlugField(max_length=100, unique=True, choices=SLUG_CHOICES)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300, blank=True)
    content = models.TextField(help_text="HTML or Markdown legal text content")
    last_updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Legal Page'
        verbose_name_plural = 'Legal Pages'

    def __str__(self):
        return self.title



