from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_mobile',
            'delivery_address', 'city', 'state', 'pincode', 'payment_method'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-input'}),
            'customer_email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-input'}),
            'customer_mobile': forms.TextInput(attrs={'placeholder': '10-Digit Mobile Number', 'class': 'form-input'}),
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'House / Flat No., Street, Landmark...', 'class': 'form-textarea'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-input'}),
            'state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-input'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Pincode', 'class': 'form-input'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-radio'}),
        }
