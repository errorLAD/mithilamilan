from django import forms
from .models import Event, EventScheduleDay, EventImportantDate

class EventSubmissionForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}))

    class Meta:
        model = Event
        fields = [
            'title', 'category', 'cover_image', 'short_description', 'about',
            'history_background', 'start_date', 'end_date', 'location',
            'venue_info', 'organizer', 'contact_info', 'map_location',
            'submitter_name', 'submitter_email'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Durga Puja 2026', 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'short_description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Brief 2-line summary of the festival or event...', 'class': 'form-textarea'}),
            'about': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detailed description of celebrations, rituals, rituals...', 'class': 'form-textarea'}),
            'history_background': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Historical background, cultural origin or significance...', 'class': 'form-textarea'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Darbhanga, Bihar', 'class': 'form-input'}),
            'venue_info': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Exact venue name, landmark, or street address...', 'class': 'form-textarea'}),
            'organizer': forms.TextInput(attrs={'placeholder': 'e.g. Mithila Cultural Association', 'class': 'form-input'}),
            'contact_info': forms.TextInput(attrs={'placeholder': 'e.g. +91 98765 43210 or email@domain.com', 'class': 'form-input'}),
            'map_location': forms.TextInput(attrs={'placeholder': 'Google Maps share link or address', 'class': 'form-input'}),
            'submitter_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'form-input'}),
            'submitter_email': forms.EmailInput(attrs={'placeholder': 'Your Contact Email', 'class': 'form-input'}),
        }
