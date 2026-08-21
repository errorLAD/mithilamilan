from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import MatrimonialProfile, ProfileReport
from .forms import MatrimonialProfileForm, ProfileReportForm

def profile_list(request):
    query = request.GET.get('q', '').strip()
    gender = request.GET.get('gender', '').strip()
    min_age = request.GET.get('min_age', '').strip()
    max_age = request.GET.get('max_age', '').strip()
    location = request.GET.get('location', '').strip()
    education = request.GET.get('education', '').strip()
    profession = request.GET.get('profession', '').strip()
    native_place = request.GET.get('native_place', '').strip()

    profiles_qs = MatrimonialProfile.objects.filter(status__in=['approved', 'published'])

    if query:
        profiles_qs = profiles_qs.filter(
            Q(full_name__icontains=query) |
            Q(education__icontains=query) |
            Q(profession__icontains=query) |
            Q(location__icontains=query) |
            Q(native_place__icontains=query) |
            Q(about_person__icontains=query)
        )

    if gender in ['male', 'female']:
        profiles_qs = profiles_qs.filter(gender=gender)

    if min_age and min_age.isdigit():
        profiles_qs = profiles_qs.filter(age__gte=int(min_age))

    if max_age and max_age.isdigit():
        profiles_qs = profiles_qs.filter(age__lte=int(max_age))

    if location:
        profiles_qs = profiles_qs.filter(location__icontains=location)

    if education:
        profiles_qs = profiles_qs.filter(education__icontains=education)

    if profession:
        profiles_qs = profiles_qs.filter(profession__icontains=profession)

    if native_place:
        profiles_qs = profiles_qs.filter(native_place__icontains=native_place)

    featured_profiles = MatrimonialProfile.objects.filter(status__in=['approved', 'published'], is_featured=True)[:3]

    paginator = Paginator(profiles_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profiles': page_obj,
        'page_obj': page_obj,
        'featured_profiles': featured_profiles,
        'query': query,
        'gender': gender,
        'min_age': min_age,
        'max_age': max_age,
        'location': location,
        'education': education,
        'profession': profession,
        'native_place': native_place,
        'total_count': profiles_qs.count(),
    }
    return render(request, 'ghatkaiti/profile_list.html', context)

def profile_detail(request, slug):
    profile = get_object_or_404(MatrimonialProfile, slug=slug)

    # Permission check for unapproved posts
    if profile.status not in ['approved', 'published']:
        if not (request.user.is_authenticated and (request.user.is_staff or request.user == profile.submitted_by)):
            messages.warning(request, "This matrimonial post is currently under admin verification.")
            return redirect('ghatkaiti:profile_list')

    report_form = ProfileReportForm()

    if request.method == 'POST' and request.POST.get('action') == 'report':
        report_form = ProfileReportForm(request.POST)
        if report_form.is_valid():
            rep = report_form.save(commit=False)
            rep.profile = profile
            if request.user.is_authenticated:
                rep.reported_by = request.user
            rep.save()
            messages.success(request, "Thank you. Your report has been submitted to Admin for safety inspection.")
            return redirect('ghatkaiti:profile_detail', slug=profile.slug)

    related_profiles = MatrimonialProfile.objects.filter(
        status__in=['approved', 'published'], gender=profile.gender
    ).exclude(pk=profile.pk)[:3]

    context = {
        'profile': profile,
        'report_form': report_form,
        'related_profiles': related_profiles,
    }
    return render(request, 'ghatkaiti/profile_detail.html', context)

def profile_create(request):
    if request.method == 'POST':
        form = MatrimonialProfileForm(request.POST, request.FILES)
        if form.is_valid():
            prof = form.save(commit=False)
            if request.user.is_authenticated:
                prof.submitted_by = request.user

            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                prof.status = 'published'
                prof.is_verified = True
                messages.success(request, f"Matrimonial profile for '{prof.full_name}' published directly!")
            else:
                prof.status = 'pending'
                messages.success(request, f"Thank you! Matrimonial post for '{prof.full_name}' has been submitted. Admin will review before public listing.")

            prof.save()
            return redirect(prof.get_absolute_url() if prof.status in ['approved', 'published'] else 'ghatkaiti:profile_list')
    else:
        form = MatrimonialProfileForm()

    return render(request, 'ghatkaiti/profile_form.html', {'form': form})
