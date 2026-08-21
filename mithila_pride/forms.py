from django import forms
from .models import MithilaPride

class MithilaPrideSubmissionForm(forms.ModelForm):
    class Meta:
        model = MithilaPride
        fields = [
            'full_name', 'category', 'era_generation', 'place_location',
            'photograph', 'biography', 'early_life', 'education', 'career',
            'major_achievements', 'awards', 'publications_work',
            'contributions_to_mithila', 'organization_institution',
            'website_social_links', 'references_sources',
            'submitter_name', 'submitter_email'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'e.g. Dr. Kameshwar Singh / Vidyapati', 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'era_generation': forms.Select(attrs={'class': 'form-select'}),
            'place_location': forms.TextInput(attrs={'placeholder': 'e.g. Madhubani / Darbhanga, Bihar', 'class': 'form-input'}),
            'biography': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detailed biography and life overview...', 'class': 'form-textarea'}),
            'early_life': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Birthplace, early schooling, family background...', 'class': 'form-textarea'}),
            'education': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Degrees, universities, tradition of learning...', 'class': 'form-textarea'}),
            'career': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Professional service, leadership roles, teaching...', 'class': 'form-textarea'}),
            'major_achievements': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Key milestones, breakthroughs, or discoveries...', 'class': 'form-textarea'}),
            'awards': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Padma Shri, Sahitya Akademi, State honors...', 'class': 'form-textarea'}),
            'publications_work': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Books authored, research publications, art compositions...', 'class': 'form-textarea'}),
            'contributions_to_mithila': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Impact on Mithila culture, Maithili literature, or community development...', 'class': 'form-textarea'}),
            'organization_institution': forms.TextInput(attrs={'placeholder': 'e.g. L.N. Mithila University', 'class': 'form-input'}),
            'website_social_links': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Wikipedia link, news links, official site...', 'class': 'form-textarea'}),
            'references_sources': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Citations or source materials...', 'class': 'form-textarea'}),
            'submitter_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'form-input'}),
            'submitter_email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'form-input'}),
        }
