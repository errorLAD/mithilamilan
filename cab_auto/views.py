from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import DriverProfile
from .forms import DriverRegistrationForm

def cab_auto_home(request):
    auto_count = DriverProfile.objects.filter(status__in=['approved', 'published'], vehicle_type='auto').count()
    taxi_count = DriverProfile.objects.filter(status__in=['approved', 'published'], vehicle_type='taxi').count()
    
    featured_drivers = DriverProfile.objects.filter(status__in=['approved', 'published'], is_featured=True)[:4]

    context = {
        'auto_count': auto_count,
        'taxi_count': taxi_count,
        'featured_drivers': featured_drivers,
    }
    return render(request, 'cab_auto/cab_auto_home.html', context)

def driver_list(request, forced_type=None):
    query = request.GET.get('q', '').strip()
    vehicle_type = forced_type or request.GET.get('type', '').strip()
    location = request.GET.get('location', '').strip()
    verified_only = request.GET.get('verified', '').strip()

    drivers_qs = DriverProfile.objects.filter(status__in=['approved', 'published'])

    if query:
        drivers_qs = drivers_qs.filter(
            Q(full_name__icontains=query) |
            Q(vehicle_model__icontains=query) |
            Q(service_area__icontains=query) |
            Q(about__icontains=query)
        )

    if vehicle_type in ['auto', 'taxi']:
        drivers_qs = drivers_qs.filter(vehicle_type=vehicle_type)

    if location:
        drivers_qs = drivers_qs.filter(service_area__icontains=location)

    if verified_only == 'true' or verified_only == '1':
        drivers_qs = drivers_qs.filter(is_verified=True)

    paginator = Paginator(drivers_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    section_title = "Local Transport Directory"
    if vehicle_type == 'auto':
        section_title = "Verified Auto & E-Rickshaw Drivers"
    elif vehicle_type == 'taxi':
        section_title = "Verified Cab & Taxi Services"

    context = {
        'drivers': page_obj,
        'page_obj': page_obj,
        'query': query,
        'vehicle_type': vehicle_type,
        'location': location,
        'verified_only': verified_only,
        'total_count': drivers_qs.count(),
        'section_title': section_title,
    }
    return render(request, 'cab_auto/driver_list.html', context)

def driver_detail(request, slug):
    driver = get_object_or_404(DriverProfile, slug=slug)

    # Check permission for unapproved profiles
    if driver.status not in ['approved', 'published']:
        if not (request.user.is_authenticated and (request.user.is_staff or request.user == driver.user)):
            messages.warning(request, "This driver profile is under admin verification.")
            return redirect('cab_auto:cab_auto_home')

    related_drivers = DriverProfile.objects.filter(
        status__in=['approved', 'published'], vehicle_type=driver.vehicle_type
    ).exclude(pk=driver.pk)[:3]

    context = {
        'driver': driver,
        'related_drivers': related_drivers,
    }
    return render(request, 'cab_auto/driver_detail.html', context)

def driver_register(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            if request.user.is_authenticated:
                driver.user = request.user

            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                driver.status = 'published'
                driver.is_verified = True
                messages.success(request, f"Driver profile for '{driver.full_name}' published directly!")
            else:
                driver.status = 'pending'
                messages.success(request, f"Thank you {driver.full_name}! Your driver listing has been submitted for Admin verification.")

            driver.save()
            return redirect(driver.get_absolute_url() if driver.status in ['approved', 'published'] else 'cab_auto:cab_auto_home')
    else:
        form = DriverRegistrationForm()

    return render(request, 'cab_auto/driver_form.html', {'form': form})
