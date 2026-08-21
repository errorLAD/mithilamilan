from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class MithilaPride(models.Model):
    CATEGORY_CHOICES = [
        ('scholar', 'Scholar'),
        ('educator', 'Educator'),
        ('artist', 'Artist'),
        ('writer', 'Writer'),
        ('researcher', 'Researcher'),
        ('cultural_personality', 'Cultural Personality'),
        ('teacher', 'Teacher'),
        ('author', 'Author'),
        ('other', 'Other Contributor'),
    ]

    ERA_CHOICES = [
        ('classical', 'Classical & Ancient Era'),
        ('20th_century', '20th Century Pioneers'),
        ('contemporary', 'Contemporary Leaders'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    full_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=285, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='scholar')
    era_generation = models.CharField(max_length=50, choices=ERA_CHOICES, default='contemporary')
    
    place_location = models.CharField(max_length=255, help_text="Native place, e.g. Madhubani / Darbhanga, Bihar")
    photograph = models.ImageField(upload_to='mithila_pride/photos/', null=True, blank=True)
    
    biography = models.TextField(help_text="Overview biography and summary of life")
    early_life = models.TextField(blank=True, help_text="Birth, childhood, and roots")
    education = models.TextField(blank=True, help_text="Academic qualifications, institutions")
    career = models.TextField(blank=True, help_text="Professional career trajectory")
    major_achievements = models.TextField(blank=True, help_text="Key achievements and milestones")
    awards = models.TextField(blank=True, help_text="Honors, Padma awards, Sahitya Akademi, etc.")
    publications_work = models.TextField(blank=True, help_text="Notable books, papers, artwork, or compositions")
    contributions_to_mithila = models.TextField(help_text="Key contributions to Mithila language, culture, society or research")
    
    organization_institution = models.CharField(max_length=255, blank=True, help_text="University, academy, or organization associated")
    website_social_links = models.TextField(blank=True, help_text="Wikipedia link, official website, or news profiles")
    references_sources = models.TextField(blank=True, help_text="Citations or reference sources")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submitted_personalities'
    )
    submitter_name = models.CharField(max_length=150, blank=True)
    submitter_email = models.EmailField(blank=True)
    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'full_name']
        verbose_name = 'Mithila Pride & Scholar'
        verbose_name_plural = 'Mithila Pride & Scholars'

    def __str__(self):
        return f"{self.full_name} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            prefix = 'scholar' if self.category == 'scholar' else 'mithila-pride'
            base_slug = slugify(f"{prefix}-{self.full_name}") or 'personality'
            slug = base_slug
            counter = 1
            while MithilaPride.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.category == 'scholar':
            return reverse('mithila_pride:scholar_detail', kwargs={'slug': self.slug})
        return reverse('mithila_pride:person_detail', kwargs={'slug': self.slug})

class MithilaPrideTimeline(models.Model):
    person = models.ForeignKey(MithilaPride, on_delete=models.CASCADE, related_name='timeline_events')
    year_or_date = models.CharField(max_length=100, help_text="e.g. 1974 or 15 August 1985")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['year_or_date']

    def __str__(self):
        return f"{self.person.full_name} - {self.year_or_date}: {self.title}"

class MithilaPrideGallery(models.Model):
    person = models.ForeignKey(MithilaPride, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='mithila_pride/gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Gallery for {self.person.full_name}"
