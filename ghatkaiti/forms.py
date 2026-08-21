from django import forms
from .models import MatrimonialProfile, ProfileReport

class MatrimonialProfileForm(forms.ModelForm):
    class Meta:
        model = MatrimonialProfile
        fields = [
            'looking_for', 'gender', 'full_name', 'age', 'height',
            'education', 'profession', 'location', 'native_place',
            'current_city', 'community_family_details', 'about_person',
            'family_info', 'expectations', 'contact_person_name',
            'whatsapp_number', 'profile_photo'
        ]
        widgets = {
            'looking_for': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Candidate Full Name', 'class': 'form-input'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age in years e.g. 27', 'class': 'form-input'}),
            'height': forms.TextInput(attrs={'placeholder': 'e.g. 5\' 9" (Optional)', 'class': 'form-input'}),
            'education': forms.TextInput(attrs={'placeholder': 'e.g. B.Tech (IIT Delhi), M.Tech', 'class': 'form-input'}),
            'profession': forms.TextInput(attrs={'placeholder': 'e.g. Senior Software Engineer / Bank Manager', 'class': 'form-input'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Delhi NCR', 'class': 'form-input'}),
            'native_place': forms.TextInput(attrs={'placeholder': 'e.g. Madhubani / Darbhanga, Bihar', 'class': 'form-input'}),
            'current_city': forms.TextInput(attrs={'placeholder': 'e.g. Noida / New Delhi / Bangalore', 'class': 'form-input'}),
            'community_family_details': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional gotra or roots details...', 'class': 'form-textarea'}),
            'about_person': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief description of candidate, nature, hobbies...', 'class': 'form-textarea'}),
            'family_info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Father\'s profession, mother, siblings, family background...', 'class': 'form-textarea'}),
            'expectations': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Partner preferences, values, educational expectations...', 'class': 'form-textarea'}),
            'contact_person_name': forms.TextInput(attrs={'placeholder': 'Parent or Guardian Full Name', 'class': 'form-input'}),
            'whatsapp_number': forms.TextInput(attrs={'placeholder': 'Mandatory WhatsApp Number for protected contact CTA', 'class': 'form-input', 'required': 'required'}),
        }

    def clean_whatsapp_number(self):
        wa = self.cleaned_data.get('whatsapp_number')
        if not wa:
            raise forms.ValidationError("WhatsApp number is required for protected matrimonial contact.")
        return wa

class ProfileReportForm(forms.ModelForm):
    class Meta:
        model = ProfileReport
        fields = ['reason', 'details', 'reporter_name', 'reporter_email']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Explain why you are reporting this profile...', 'class': 'form-textarea'}),
            'reporter_name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-input'}),
            'reporter_email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-input'}),
        }
