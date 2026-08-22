import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

INPUT_CLASSES = 'w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-[#E85D2A]/20 focus:border-[#E85D2A] focus:bg-white transition-all'

class CustomUserCreationForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Full Name',
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'e.g. Ramesh Kumar Jha'
        })
    )
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Choose a unique username',
            'autocomplete': 'username'
        })
    )
    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'you@example.com',
            'autocomplete': 'email'
        })
    )
    location = forms.CharField(
        label='Location',
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'e.g. Darbhanga / New Delhi'
        })
    )
    avatar = forms.ImageField(
        label='Profile Picture',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-xs text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-[#E85D2A] hover:file:bg-orange-100 cursor-pointer'
        })
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'At least 8 characters',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Re-enter your password',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'location', 'avatar')

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError("Username cannot be empty.")
        
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
            
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, underscores, hyphens, and dots.")
            
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
            
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("Email address is required.")
            
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
            
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Passwords do not match. Please try again.")
            else:
                # Use Django's password validation
                dummy_user = CustomUser(username=username) if username else None
                try:
                    validate_password(password1, user=dummy_user)
                except ValidationError as error:
                    self.add_error('password1', error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        full_name = self.cleaned_data.get('full_name', '').strip()
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
                
        user.location = self.cleaned_data.get('location', '')
        
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='Username or Email',
        required=True,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter username or email address',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
    )
    remember_me = forms.BooleanField(
        label='Remember me',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-[#E85D2A] bg-slate-50 border-slate-300 rounded focus:ring-[#E85D2A] focus:ring-2'
        })
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'location', 'avatar', 'bio')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'location', 'bio', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'bio': forms.Textarea(attrs={'class': f'{INPUT_CLASSES} h-24'}),
            'avatar': forms.FileInput(attrs={'class': 'block w-full text-xs text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-[#E85D2A]'}),
        }
