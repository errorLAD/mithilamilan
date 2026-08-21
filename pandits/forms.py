from django import forms
from .models import PanditProfile, ConsultationRequest

class PanditOnboardingForm(forms.ModelForm):
    class Meta:
        model = PanditProfile
        fields = [
            'full_name', 'profile_type', 'profile_photo', 'designation',
            'whatsapp_number', 'phone_number', 'location', 'address_area',
            'experience_years', 'languages', 'specialization',
            'services_offered', 'about', 'availability', 'service_pricing'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'e.g. Pandit Rameshwar Jha', 'class': 'form-input'}),
            'profile_type': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.TextInput(attrs={'placeholder': 'e.g. Vedic Karma Kanda & Vastu Specialist', 'class': 'form-input'}),
            'whatsapp_number': forms.TextInput(attrs={'placeholder': 'Mandatory e.g. 9876543210', 'class': 'form-input', 'required': 'required'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Alternative phone number', 'class': 'form-input'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Darbhanga, Bihar / Delhi NCR', 'class': 'form-input'}),
            'address_area': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Neighborhood, temple, or full address...', 'class': 'form-textarea'}),
            'experience_years': forms.NumberInput(attrs={'placeholder': '10', 'class': 'form-input'}),
            'languages': forms.TextInput(attrs={'placeholder': 'e.g. Maithili, Hindi, Sanskrit, English', 'class': 'form-input'}),
            'specialization': forms.TextInput(attrs={'placeholder': 'e.g. Griha Pravesh, Vivah Puja, Janam Kundali', 'class': 'form-input'}),
            'services_offered': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of services, rituals, pujas or horoscopes offered...', 'class': 'form-textarea'}),
            'about': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your educational lineage, experience, and background...', 'class': 'form-textarea'}),
            'availability': forms.TextInput(attrs={'placeholder': 'e.g. Mon - Sun: 8:00 AM - 8:00 PM', 'class': 'form-input'}),
            'service_pricing': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional pricing rates e.g. Kundali: ₹501', 'class': 'form-textarea'}),
        }

    def clean_whatsapp_number(self):
        wa = self.cleaned_data.get('whatsapp_number')
        if not wa:
            raise forms.ValidationError("WhatsApp number is mandatory for onboarding.")
        return wa

class ConsultationRequestForm(forms.ModelForm):
    preferred_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}))

    class Meta:
        model = ConsultationRequest
        fields = [
            'user_name', 'user_phone', 'user_whatsapp', 'service_required',
            'preferred_date', 'preferred_time', 'location_type', 'message'
        ]
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'form-input'}),
            'user_phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'form-input'}),
            'user_whatsapp': forms.TextInput(attrs={'placeholder': 'Your WhatsApp Number', 'class': 'form-input'}),
            'service_required': forms.TextInput(attrs={'placeholder': 'e.g. Griha Pravesh Puja / Kundali Reading', 'class': 'form-input'}),
            'preferred_time': forms.TextInput(attrs={'placeholder': 'e.g. 10:00 AM', 'class': 'form-input'}),
            'location_type': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any specific details or requirements...', 'class': 'form-textarea'}),
        }
