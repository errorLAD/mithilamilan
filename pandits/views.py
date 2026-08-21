from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from urllib.parse import quote
from .models import PanditProfile, PanditGallery, ConsultationRequest
from .forms import PanditOnboardingForm, ConsultationRequestForm

def profile_list(request, forced_type=None):
    query = request.GET.get('q', '').strip()
    profile_type = forced_type or request.GET.get('type', '').strip()
    location = request.GET.get('location', '').strip()
    specialization = request.GET.get('specialization', '').strip()
    language = request.GET.get('language', '').strip()
    min_exp = request.GET.get('exp', '').strip()
    verified_only = request.GET.get('verified', '').strip()

    profiles_qs = PanditProfile.objects.filter(status__in=['approved', 'published'])

    if query:
        profiles_qs = profiles_qs.filter(
            Q(full_name__icontains=query) |
            Q(designation__icontains=query) |
            Q(specialization__icontains=query) |
            Q(services_offered__icontains=query) |
            Q(location__icontains=query)
        )

    if profile_type:
        if profile_type in ['pandit', 'astrologer']:
            profiles_qs = profiles_qs.filter(Q(profile_type=profile_type) | Q(profile_type='both'))

    if location:
        profiles_qs = profiles_qs.filter(location__icontains=location)

    if specialization:
        profiles_qs = profiles_qs.filter(specialization__icontains=specialization)

    if language:
        profiles_qs = profiles_qs.filter(languages__icontains=language)

    if min_exp and min_exp.isdigit():
        profiles_qs = profiles_qs.filter(experience_years__gte=int(min_exp))

    if verified_only == 'true' or verified_only == '1':
        profiles_qs = profiles_qs.filter(is_verified=True)

    featured_profiles = PanditProfile.objects.filter(status__in=['approved', 'published'], is_featured=True)[:4]

    paginator = Paginator(profiles_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    section_title = "Pandit & Astrologer Directory"
    if profile_type == 'pandit':
        section_title = "Verified Pandits in Mithila & NCR"
    elif profile_type == 'astrologer':
        section_title = "Certified Astrologers & Jyotish Acharyas"

    context = {
        'profiles': page_obj,
        'page_obj': page_obj,
        'featured_profiles': featured_profiles,
        'query': query,
        'profile_type': profile_type,
        'location': location,
        'specialization': specialization,
        'language': language,
        'min_exp': min_exp,
        'verified_only': verified_only,
        'total_count': profiles_qs.count(),
        'section_title': section_title,
    }
    return render(request, 'pandits/profile_list.html', context)

def profile_detail(request, slug):
    profile = get_object_or_404(PanditProfile, slug=slug)

    # Check status permissions
    if profile.status not in ['approved', 'published']:
        if not (request.user.is_authenticated and (request.user.is_staff or request.user == profile.user)):
            messages.warning(request, "This profile is currently under admin verification.")
            return redirect('pandits:profile_list')

    gallery = profile.gallery_images.all()
    consultation_form = ConsultationRequestForm()

    if request.method == 'POST':
        consultation_form = ConsultationRequestForm(request.POST)
        if consultation_form.is_valid():
            req_item = consultation_form.save(commit=False)
            req_item.profile = profile
            if request.user.is_authenticated:
                req_item.user = request.user
            req_item.save()

            messages.success(request, f"Your consultation request for {profile.full_name} has been sent successfully!")
            
            # Format custom WhatsApp message with request payload
            wa_text = f"Namaste {profile.full_name} ji,\n\nI have requested a consultation on Mithila Platform:\n" \
                      f"- Service: {req_item.service_required}\n" \
                      f"- Preferred Date: {req_item.preferred_date}\n" \
                      f"- Time: {req_item.preferred_time or 'Anytime'}\n" \
                      f"- Mode: {req_item.get_location_type_display()}\n" \
                      f"- Name: {req_item.user_name}\n" \
                      f"- Message: {req_item.message}\n\nPlease confirm availability."

            whatsapp_url = profile.get_whatsapp_url(prefilled_text=wa_text)
            return redirect(whatsapp_url)

    # General WhatsApp launch URL
    default_wa_text = f"Namaste {profile.full_name} ji, I found your profile on Mithila Platform ({request.build_absolute_uri()}) and would like to inquire about your services."
    default_whatsapp_url = profile.get_whatsapp_url(prefilled_text=default_wa_text)

    # Related profiles
    related_profiles = PanditProfile.objects.filter(
        status__in=['approved', 'published']
    ).exclude(pk=profile.pk).filter(
        Q(location__icontains=profile.location.split(',')[0]) | Q(profile_type=profile.profile_type)
    )[:3]

    context = {
        'profile': profile,
        'gallery': gallery,
        'consultation_form': consultation_form,
        'default_whatsapp_url': default_whatsapp_url,
        'related_profiles': related_profiles,
    }
    return render(request, 'pandits/profile_detail.html', context)

def profile_onboard(request):
    if request.method == 'POST':
        form = PanditOnboardingForm(request.POST, request.FILES)
        if form.is_valid():
            prof = form.save(commit=False)
            if request.user.is_authenticated:
                prof.user = request.user
            
            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                prof.status = 'published'
                prof.is_verified = True
                messages.success(request, f"Profile for '{prof.full_name}' created and published successfully!")
            else:
                prof.status = 'pending'
                messages.success(request, f"Thank you {prof.full_name}! Your profile has been submitted. Admin will review and verify your profile shortly.")
            
            prof.save()
            return redirect(prof.get_absolute_url() if prof.status in ['approved', 'published'] else 'pandits:profile_list')
    else:
        form = PanditOnboardingForm()

    return render(request, 'pandits/onboard_form.html', {'form': form})
