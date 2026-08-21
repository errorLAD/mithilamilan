from django.db import models
from django.conf import settings
from django.utils.text import slugify

class PanchangSource(models.Model):
    name = models.CharField(max_length=255, default="मैथिली पंचांग (उर्वशी प्रकाशन)")
    year_label = models.CharField(max_length=100, default="२०२६ - २०२७ ई० (१४३४ साल)")
    publisher = models.CharField(max_length=255, default="उर्वशी प्रकाशन, पटना")
    editor = models.CharField(max_length=255, default="पं० सचिदानन्द झा (गणित, फलित)")
    compiler = models.CharField(max_length=255, default="पं० गोपीकान्त झा")
    description = models.TextField(blank=True, default="मिथिलादेशीय मकरन्दानुसार मैथिली पंचांग")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.year_label}"


class ScannedPanchangPage(models.Model):
    source = models.ForeignKey(PanchangSource, on_delete=models.CASCADE, related_name='scanned_pages', null=True, blank=True)
    page_number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255, help_text="Path to scanned page image, e.g. panch_ocr/page-02.jpg")
    ocr_text = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['page_number']

    def __str__(self):
        return f"पृष्ठ {self.page_number} - {self.title}"


class PanchangYear(models.Model):
    gregorian_year = models.IntegerField(default=2026, help_text="Starting Gregorian Year")
    title_hi = models.CharField(max_length=255, default="सन १४३४ साल (अंग्रेजी २०२६ - २०२७ ई०)")
    vikram_samvat = models.CharField(max_length=100, default="२०८३-८४")
    saka_samvat = models.CharField(max_length=100, default="१९४८")
    king_planet = models.CharField(max_length=100, default="शनि")
    minister_planet = models.CharField(max_length=100, default="मंगल")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title_hi


class PanchangMonth(models.Model):
    year = models.ForeignKey(PanchangYear, on_delete=models.CASCADE, related_name='months', null=True, blank=True)
    name_hi = models.CharField(max_length=100)
    name_mai = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100)
    month_order = models.PositiveSmallIntegerField(help_text="1 to 12")
    gregorian_range_hi = models.CharField(max_length=100, help_text="e.g. जुलाई – अगस्त")
    gregorian_range_en = models.CharField(max_length=100, help_text="e.g. July – August")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['month_order']

    def __str__(self):
        return f"{self.name_hi} ({self.gregorian_range_hi})"


class PanchangDay(models.Model):
    date = models.DateField(unique=True)
    mithila_month = models.ForeignKey(PanchangMonth, on_delete=models.SET_NULL, null=True, blank=True, related_name='days')
    mithila_month_name = models.CharField(max_length=100, blank=True)
    mithila_tithi_name = models.CharField(max_length=100, default="प्रतिपदा")
    paksha = models.CharField(max_length=50, choices=[('शुक्ल', 'शुक्ल पक्ष'), ('कृष्ण', 'कृष्ण पक्ष')], default='शुक्ल')
    tithi_end_time = models.CharField(max_length=100, blank=True, help_text="e.g. रा. ०९।४९ या 09:49 PM")
    nakshatra_name = models.CharField(max_length=100, default="रोहिणी")
    nakshatra_end_time = models.CharField(max_length=100, blank=True)
    yoga_name = models.CharField(max_length=100, blank=True, default="सिद्ध")
    karana_name = models.CharField(max_length=100, blank=True, default="बव")
    weekday_name = models.CharField(max_length=50, default="बुधवार")
    
    # Astronomical timings
    sunrise = models.CharField(max_length=50, default="05:30 AM")
    sunset = models.CharField(max_length=50, default="06:45 PM")
    moonrise = models.CharField(max_length=50, default="07:15 PM")
    moonset = models.CharField(max_length=50, default="06:10 AM")
    sun_rashi = models.CharField(max_length=100, default="सिंह")
    moon_rashi = models.CharField(max_length=100, default="कन्या")

    # Auspicious / Inauspicious periods
    abhijit_muhurta = models.CharField(max_length=100, default="11:48 AM – 12:40 PM")
    rahukaal = models.CharField(max_length=100, default="12:20 PM – 01:55 PM")
    yamaganda = models.CharField(max_length=100, default="07:10 AM – 08:45 AM")
    gulika = models.CharField(max_length=100, default="10:30 AM – 12:00 PM")

    is_amavasya = models.BooleanField(default=False)
    is_purnima = models.BooleanField(default=False)
    special_observances = models.TextField(blank=True, help_text="Special vrat, festival, or notes for the day")
    source_page = models.ForeignKey(ScannedPanchangPage, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.mithila_month_name} {self.paksha} {self.mithila_tithi_name}"


class Festival(models.Model):
    CATEGORY_CHOICES = [
        ('pabni_tihar', 'पाबनि-तिहार (Pabni-Tihar)'),
        ('vrat', 'व्रत (Vrat)'),
        ('puja', 'पूजा (Puja)'),
        ('mithila_special', 'मिथिला विशेष (Mithila Special)'),
        ('religious', 'धार्मिक (Religious)'),
        ('cultural', 'सांस्कृतिक (Cultural)'),
    ]

    title_hi = models.CharField(max_length=200)
    title_mai = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    mithila_month = models.ForeignKey(PanchangMonth, on_delete=models.SET_NULL, null=True, blank=True)
    mithila_month_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='pabni_tihar')
    short_description = models.TextField()
    traditions = models.TextField(blank=True)
    puja_vrat_info = models.TextField(blank=True)
    related_event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True, help_text="Connect to existing Events & Festivals entry")
    source_page = models.ForeignKey(ScannedPanchangPage, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title_hi} ({self.date})"


class MuhuratCategory(models.Model):
    name_hi = models.CharField(max_length=100)
    name_mai = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="fa-calendar-check", help_text="FontAwesome class e.g. fa-ring, fa-scissors, fa-om")
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order', 'name_hi']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name_hi)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_hi


class MuhuratDate(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('NEEDS_REVIEW', 'Needs Review'),
        ('VERIFIED', 'Verified'),
        ('PUBLISHED', 'Published'),
    ]

    category = models.ForeignKey(MuhuratCategory, on_delete=models.CASCADE, related_name='muhurat_dates')
    gregorian_date = models.DateField()
    mithila_month = models.ForeignKey(PanchangMonth, on_delete=models.SET_NULL, null=True, blank=True)
    mithila_month_name = models.CharField(max_length=100, blank=True)
    paksha = models.CharField(max_length=50, blank=True, help_text="e.g. कृष्ण, शुक्ल")
    tithi_name = models.CharField(max_length=100, blank=True, help_text="e.g. प्रतिपदा, द्वितीया")
    weekday_name = models.CharField(max_length=50, blank=True, help_text="e.g. बुधवार, शुक्रवार")
    nakshatra_name = models.CharField(max_length=100, blank=True, help_text="e.g. रोहिणी, हस्त")
    
    start_time = models.CharField(max_length=100, blank=True, help_text="Optional clock time string e.g. 06:30 AM")
    end_time = models.CharField(max_length=100, blank=True, help_text="Optional end time string")
    is_full_day_muhurat = models.BooleanField(default=True, help_text="True if exact clock time is not provided by source (shows 'विवाहक दिन' / full day)")
    
    notes = models.TextField(blank=True, help_text="Source notes, e.g. (छ०), (क्ष०वै०), दिवा/रात्र")
    source_page = models.ForeignKey(ScannedPanchangPage, on_delete=models.SET_NULL, null=True, blank=True)
    source_reference_text = models.CharField(max_length=255, default="मैथिली पंचांग, पृष्ठ २")
    
    verification_status = models.CharField(max_length=30, choices=VERIFICATION_STATUS_CHOICES, default='PUBLISHED')
    is_published = models.BooleanField(default=True)
    
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='entered_muhurats')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_muhurats')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['gregorian_date']

    def __str__(self):
        return f"{self.category.name_hi} - {self.gregorian_date} ({self.mithila_month_name} {self.tithi_name})"


class PanchangAuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Created Record'),
        ('UPDATE', 'Updated Record'),
        ('VERIFY', 'Verified Record'),
        ('PUBLISH', 'Published Record'),
    ]

    record_type = models.CharField(max_length=100)
    record_id = models.PositiveIntegerField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} on {self.record_type} #{self.record_id} at {self.timestamp}"


class MithilaSong(models.Model):
    video_id = models.CharField(max_length=100, unique=True, help_text="YouTube Video ID e.g. H501incNC74")
    title = models.CharField(max_length=255)
    singer = models.CharField(max_length=255, blank=True, help_text="Singer / Channel Name")
    category = models.CharField(max_length=100, default="पारम्परिक मैथिली गीत")
    audio_url = models.CharField(max_length=500, blank=True, help_text="Direct MP3 Audio URL if available")
    order = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.video_id})"

    @property
    def thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.video_id}/hqdefault.jpg"

