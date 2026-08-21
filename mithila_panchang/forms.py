from django import forms
from .models import PanchangDay, Festival, MuhuratDate, ScannedPanchangPage

class PanchangDayForm(forms.ModelForm):
    class Meta:
        model = PanchangDay
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'special_observances': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class FestivalForm(forms.ModelForm):
    class Meta:
        model = Festival
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'traditions': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'puja_vrat_info': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class MuhuratDateForm(forms.ModelForm):
    class Meta:
        model = MuhuratDate
        fields = '__all__'
        widgets = {
            'gregorian_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
