from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileUpdateForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.backend = 'users.backends.EmailOrUsernameModelBackend'
            login(request, user)
            messages.success(request, 'मिथिला परिवार में स्वागत अछि! ❤️ Welcome to MithilaMilan')
            
            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {
        'form': form,
        'next': next_url
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', True)

            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Expire on browser close

                messages.success(request, f'Welcome back, {user.username}!')

                if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                if user.is_staff or user.is_superuser:
                    return redirect('admin_panel:dashboard')
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid username/email or password. Please check your credentials.')
    else:
        form = CustomLoginForm()

    return render(request, 'users/login.html', {
        'form': form,
        'next': next_url
    })

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out safely.')
    return redirect('core:home')

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(CustomUser, username=username)
    else:
        user = request.user
    return render(request, 'users/profile.html', {'profile_user': user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:my_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})