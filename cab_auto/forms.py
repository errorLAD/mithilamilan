from django import forms
from .models import DriverProfile

class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = [
            'full_name', 'photo', 'age', 'mobile_number', 'whatsapp_number',
            'vehicle_type', 'vehicle_model', 'vehicle_number',
            'service_area', 'experience_years', 'available_hours', 'about'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Driver Full Name', 'class': 'form-input'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age e.g. 32', 'class': 'form-input'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Direct Phone Number', 'class': 'form-input'}),
            'whatsapp_number': forms.TextInput(attrs={'placeholder': 'Mandatory WhatsApp Number', 'class': 'form-input', 'required': 'required'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_model': forms.TextInput(attrs={'placeholder': 'e.g. Bajaj Maxima Auto / Dzire AC Cab', 'class': 'form-input'}),
            'vehicle_number': forms.TextInput(attrs={'placeholder': 'e.g. BR-07-PA-1234 (Optional)', 'class': 'form-input'}),
            'service_area': forms.TextInput(attrs={'placeholder': 'e.g. Darbhanga Station, Airport, Madhubani', 'class': 'form-input'}),
            'experience_years': forms.NumberInput(attrs={'placeholder': 'Years of driving experience', 'class': 'form-input'}),
            'available_hours': forms.TextInput(attrs={'placeholder': 'e.g. 24/7 or 6:00 AM - 10:00 PM', 'class': 'form-input'}),
            'about': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Routes covered, special services, outstation trips...', 'class': 'form-textarea'}),
        }

    def clean_whatsapp_number(self):
        wa = self.cleaned_data.get('whatsapp_number')
        if not wa:
            raise forms.ValidationError("WhatsApp number is mandatory for driver listing.")
        return wa
