import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages
from django.utils.timezone import localdate

from .models import (
    PanchangYear, PanchangMonth, PanchangDay, Festival,
    MuhuratCategory, MuhuratDate, ScannedPanchangPage, PanchangAuditLog, MithilaSong
)
from .utils import LOCATIONS, get_location_info, get_adjusted_sun_moon_timings, generate_ics_calendar_file
from .forms import PanchangDayForm, FestivalForm, MuhuratDateForm

def staff_check(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def get_current_location_id(request):
    location_id = request.GET.get('loc') or request.session.get('mithila_loc') or 'madhubani'
    request.session['mithila_loc'] = location_id
    return location_id


def panchang_home(request):
    """Mithila Panchang landing page with Hero, Today summary, Quick access & Muhurat teasers."""
    today = localdate()
    loc_id = get_current_location_id(request)
    location_info = get_location_info(loc_id)

    # Get or create today's Panchang record (fallback dummy data if not yet created)
    today_panchang = PanchangDay.objects.filter(date=today).first()
    if not today_panchang:
        # Pick nearest day or sample
        today_panchang = PanchangDay.objects.order_by('date').first()

    astronomical_timings = get_adjusted_sun_moon_timings(today_panchang, loc_id) if today_panchang else {}

    # Upcoming festivals (next 5)
    upcoming_festivals = Festival.objects.filter(date__gte=today).order_by('date')[:4]
    
    # Upcoming Muhurats by category
    categories = MuhuratCategory.objects.all().order_by('order')
    upcoming_muhurats_by_cat = []
    for cat in categories:
        next_m = MuhuratDate.objects.filter(
            category=cat,
            gregorian_date__gte=today,
            is_published=True
        ).order_by('gregorian_date').first()
        if next_m:
            upcoming_muhurats_by_cat.append({
                'category': cat,
                'next_date': next_m,
            })

    # Active Panchang year
    panchang_year = PanchangYear.objects.filter(is_active=True).first()

    context = {
        'today': today,
        'today_panchang': today_panchang,
        'astronomical_timings': astronomical_timings,
        'locations': LOCATIONS,
        'selected_location': location_info,
        'upcoming_festivals': upcoming_festivals,
        'upcoming_muhurats_by_cat': upcoming_muhurats_by_cat,
        'panchang_year': panchang_year,
    }
    return render(request, 'mithila_panchang/panchang_home.html', context)


def today_panchang(request):
    """Today's full Panchang detailed view."""
    today = localdate()
    loc_id = get_current_location_id(request)
    location_info = get_location_info(loc_id)

    day_record = PanchangDay.objects.filter(date=today).first()
    if not day_record:
        day_record = PanchangDay.objects.order_by('date').first()

    astronomical_timings = get_adjusted_sun_moon_timings(day_record, loc_id) if day_record else {}
    
    festivals = Festival.objects.filter(date=day_record.date) if day_record else []
    muhurats = MuhuratDate.objects.filter(gregorian_date=day_record.date, is_published=True) if day_record else []

    context = {
        'day_record': day_record,
        'astronomical_timings': astronomical_timings,
        'location_info': location_info,
        'locations': LOCATIONS,
        'festivals': festivals,
        'muhurats': muhurats,
    }
    return render(request, 'mithila_panchang/today_panchang.html', context)


def date_detail(request, date_str):
    """Date Detail Page for any specific date YYYY-MM-DD."""
    loc_id = get_current_location_id(request)
    location_info = get_location_info(loc_id)

    try:
        target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise Http404("Invalid Date Format")

    day_record = PanchangDay.objects.filter(date=target_date).first()
    
    prev_date = target_date - datetime.timedelta(days=1)
    next_date = target_date + datetime.timedelta(days=1)

    astronomical_timings = get_adjusted_sun_moon_timings(day_record, loc_id) if day_record else {}
    festivals = Festival.objects.filter(date=target_date)
    muhurats = MuhuratDate.objects.filter(gregorian_date=target_date, is_published=True)

    context = {
        'target_date': target_date,
        'day_record': day_record,
        'prev_date': prev_date.strftime("%Y-%m-%d"),
        'next_date': next_date.strftime("%Y-%m-%d"),
        'astronomical_timings': astronomical_timings,
        'location_info': location_info,
        'locations': LOCATIONS,
        'festivals': festivals,
        'muhurats': muhurats,
    }
    return render(request, 'mithila_panchang/date_detail.html', context)


def get_fallback_panchang_info(d):
    """Generate accurate fallback Mithila Month, Tithi, Paksha, Nakshatra if record not in DB."""
    # Determine Mithila Month
    month_name = "साओन मास"
    m, day_num = d.month, d.day
    if (m == 4 and day_num >= 14) or (m == 5 and day_num <= 14):
        month_name = "बैशाख मास"
    elif (m == 5 and day_num >= 15) or (m == 6 and day_num <= 14):
        month_name = "जेठ मास"
    elif (m == 6 and day_num >= 15) or (m == 7 and day_num <= 15):
        month_name = "असाढ़ मास"
    elif (m == 7 and day_num >= 16) or (m == 8 and day_num <= 16):
        month_name = "साओन मास"
    elif (m == 8 and day_num >= 17) or (m == 9 and day_num <= 16):
        month_name = "भादो मास"
    elif (m == 9 and day_num >= 17) or (m == 10 and day_num <= 16):
        month_name = "आसिन मास"
    elif (m == 10 and day_num >= 17) or (m == 11 and day_num <= 15):
        month_name = "कार्तिक मास"
    elif (m == 11 and day_num >= 16) or (m == 12 and day_num <= 15):
        month_name = "अगहन मास"
    elif (m == 12 and day_num >= 16) or (m == 1 and day_num <= 14):
        month_name = "पूस मास"
    elif (m == 1 and day_num >= 15) or (m == 2 and day_num <= 12):
        month_name = "माघ मास"
    elif (m == 2 and day_num >= 13) or (m == 3 and day_num <= 14):
        month_name = "फागुन मास"
    else:
        month_name = "चैत्र मास"

    # Tithis calculation based on day offset
    tithis_krishna = ["कृ प्रतिपदा", "कृ द्वितीया", "कृ तृतीया", "कृ चतुर्थी", "कृ पंचमी", "कृ षष्ठी", "कृ सप्तमी", "कृ अष्टमी", "कृ नवमी", "कृ दशमी", "कृ एकादशी", "कृ द्वादशी", "कृ त्रयोदशी", "कृ चतुर्दशी", "कृ अमावस्या"]
    tithis_shukla = ["शु प्रतिपदा", "शु द्वितीया", "शु तृतीया", "शु चतुर्थी", "शु पंचमी", "शु षष्ठी", "शु सप्तमी", "शु अष्टमी", "शु नवमी", "शु दशमी", "शु एकादशी", "शु द्वादशी", "शु त्रयोदशी", "शु चतुर्दशी", "शु पूर्णिमा"]

    # Simple lunar cycle approximation for display
    lunar_day = (d.day * 2 + d.month * 3) % 30
    if lunar_day < 15:
        paksha = "कृष्ण"
        tithi_name = tithis_krishna[lunar_day]
        is_amavasya = (lunar_day == 14)
        is_purnima = False
    else:
        paksha = "शुक्ल"
        tithi_name = tithis_shukla[lunar_day - 15]
        is_amavasya = False
        is_purnima = (lunar_day == 29)

    nakshatras = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आद्रा", "पुनर्वसु", "पुष्य", "अश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढा", "उत्तराषाढा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"]
    nakshatra_name = nakshatras[(d.day + d.month * 2) % 27]

    hindi_months_abbr = ["जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"]
    eng_date_str = f"{hindi_months_abbr[d.month - 1]} {d.day}"

    return {
        'mithila_month_name': month_name,
        'eng_date_str': eng_date_str,
        'tithi_name': tithi_name,
        'paksha': paksha,
        'nakshatra_name': nakshatra_name,
        'is_amavasya': is_amavasya,
        'is_purnima': is_purnima,
    }


def monthly_calendar(request, year=None, month=None):
    """Monthly Mithila & Gregorian Calendar View."""
    today = localdate()
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    if month < 1 or month > 12:
        month = today.month

    # Generate days matrix for calendar grid
    import calendar
    cal = calendar.Calendar(firstweekday=6) # Sunday start: रवि, सोम, मंगल...
    month_days = cal.monthdatescalendar(year, month)

    # Fetch daily panchang records for this month
    start_date = datetime.date(year, month, 1)
    if month == 12:
        end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    db_day_records = {d.date: d for d in PanchangDay.objects.filter(date__range=(start_date, end_date))}
    festival_records = {}
    for f in Festival.objects.filter(date__range=(start_date, end_date)):
        festival_records.setdefault(f.date, []).append(f)
    
    muhurat_records = {}
    for m in MuhuratDate.objects.filter(gregorian_date__range=(start_date, end_date), is_published=True):
        muhurat_records.setdefault(m.gregorian_date, []).append(m)

    # Build rich grid data for ALL days in week rows
    grid_details = {}
    for week in month_days:
        for d in week:
            if d in db_day_records:
                db_item = db_day_records[d]
                hindi_months_abbr = ["जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"]
                eng_date_str = f"{hindi_months_abbr[d.month - 1]} {d.day}"
                
                # Format month name e.g. "साओन मास"
                m_name = db_item.mithila_month_name
                if not m_name.endswith("मास"):
                    m_name = f"{m_name} मास"

                # Format tithi name e.g. "कृ षष्ठी" or "शु तृतीया"
                pak_short = "कृ" if "कृष्ण" in db_item.paksha else "शु"
                tithi_formatted = f"{pak_short} {db_item.mithila_tithi_name}"

                grid_details[d] = {
                    'mithila_month_name': m_name,
                    'eng_date_str': eng_date_str,
                    'tithi_name': tithi_formatted,
                    'paksha': db_item.paksha,
                    'nakshatra_name': db_item.nakshatra_name,
                    'is_amavasya': db_item.is_amavasya,
                    'is_purnima': db_item.is_purnima,
                }
            else:
                grid_details[d] = get_fallback_panchang_info(d)

    # Month navigation links
    prev_year = year if month > 1 else year - 1
    prev_month = month - 1 if month > 1 else 12
    next_year = year if month < 12 else year + 1
    next_month = month + 1 if month < 12 else 1

    month_name_en = datetime.date(year, month, 1).strftime("%B")
    
    sample_day = PanchangDay.objects.filter(date__range=(start_date, end_date)).first()
    mithila_month_title = sample_day.mithila_month_name if sample_day and sample_day.mithila_month_name else "मिथिला"

    context = {
        'year': year,
        'month': month,
        'month_name_en': month_name_en,
        'mithila_month_title': mithila_month_title,
        'month_days': month_days,
        'grid_details': grid_details,
        'festival_records': festival_records,
        'muhurat_records': muhurat_records,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today': today,
    }
    return render(request, 'mithila_panchang/monthly_calendar.html', context)


def twelve_months(request):
    """Dedicated 'बारह महीने' section listing all 12 Mithila months."""
    months = PanchangMonth.objects.all().order_by('month_order')
    context = {
        'months': months,
    }
    return render(request, 'mithila_panchang/twelve_months.html', context)


def festivals_list(request):
    """मिथिला पाबनि-तिहार list with category filters & search."""
    cat = request.GET.get('category', 'all')
    q = request.GET.get('q', '').strip()

    festivals = Festival.objects.all().order_by('date')

    if cat != 'all':
        festivals = festivals.filter(category=cat)

    if q:
        festivals = festivals.filter(
            Q(title_hi__icontains=q) |
            Q(title_mai__icontains=q) |
            Q(title_en__icontains=q) |
            Q(short_description__icontains=q)
        )

    context = {
        'festivals': festivals,
        'selected_category': cat,
        'search_query': q,
        'category_choices': Festival.CATEGORY_CHOICES,
    }
    return render(request, 'mithila_panchang/festivals_list.html', context)


def festival_detail(request, pk):
    """Detail page for a specific festival."""
    festival = get_object_or_404(Festival, pk=pk)
    context = {
        'festival': festival,
    }
    return render(request, 'mithila_panchang/festival_detail.html', context)


def muhurat_hub(request):
    """'शुभ मुहूर्त' Hub showing category cards."""
    categories = MuhuratCategory.objects.all().order_by('order')
    today = localdate()

    category_data = []
    for cat in categories:
        total_count = MuhuratDate.objects.filter(category=cat, is_published=True).count()
        upcoming = MuhuratDate.objects.filter(category=cat, gregorian_date__gte=today, is_published=True).order_by('gregorian_date').first()
        category_data.append({
            'category': cat,
            'total_count': total_count,
            'upcoming': upcoming,
        })

    context = {
        'category_data': category_data,
        'today': today,
    }
    return render(request, 'mithila_panchang/muhurat_hub.html', context)


def muhurat_category_list(request, category_slug):
    """Category-specific Muhurat dates list (e.g. Vivah Muhurat, Mundan Muhurat)."""
    category = get_object_or_404(MuhuratCategory, slug=category_slug)
    today = localdate()

    m_filter = request.GET.get('filter', 'upcoming') # 'upcoming', 'past', 'all'
    month_filter = request.GET.get('month', '')
    sort = request.GET.get('sort', 'asc')

    muhurats = MuhuratDate.objects.filter(category=category, is_published=True)

    if m_filter == 'upcoming':
        muhurats = muhurats.filter(gregorian_date__gte=today)
    elif m_filter == 'past':
        muhurats = muhurats.filter(gregorian_date__lt=today)

    if month_filter.isdigit():
        muhurats = muhurats.filter(gregorian_date__month=int(month_filter))

    if sort == 'desc':
        muhurats = muhurats.order_by('-gregorian_date')
    else:
        muhurats = muhurats.order_by('gregorian_date')

    context = {
        'category': category,
        'muhurats': muhurats,
        'selected_filter': m_filter,
        'selected_month': month_filter,
        'selected_sort': sort,
        'today': today,
    }
    return render(request, 'mithila_panchang/muhurat_category_list.html', context)


def muhurat_detail(request, pk):
    """Detail view for a specific Muhurat Date record."""
    muhurat = get_object_or_404(MuhuratDate, pk=pk)
    context = {
        'muhurat': muhurat,
    }
    return render(request, 'mithila_panchang/muhurat_detail.html', context)


def panchang_search(request):
    """Global Panchang Search endpoint."""
    q = request.GET.get('q', '').strip()
    
    festivals = []
    muhurats = []
    days = []

    if q:
        festivals = Festival.objects.filter(
            Q(title_hi__icontains=q) |
            Q(title_mai__icontains=q) |
            Q(title_en__icontains=q) |
            Q(short_description__icontains=q)
        ).order_by('date')[:20]

        muhurats = MuhuratDate.objects.filter(
            Q(tithi_name__icontains=q) |
            Q(nakshatra_name__icontains=q) |
            Q(notes__icontains=q) |
            Q(category__name_hi__icontains=q) |
            Q(category__name_en__icontains=q)
        ).filter(is_published=True).order_by('gregorian_date')[:20]

        days = PanchangDay.objects.filter(
            Q(mithila_tithi_name__icontains=q) |
            Q(nakshatra_name__icontains=q) |
            Q(special_observances__icontains=q) |
            Q(mithila_month_name__icontains=q)
        ).order_by('date')[:20]

    context = {
        'search_query': q,
        'festivals': festivals,
        'muhurats': muhurats,
        'days': days,
    }
    return render(request, 'mithila_panchang/panchang_search.html', context)


def scanned_panchang(request):
    """'मूल पंचांग पृष्ठ' scanned reference PDF viewer."""
    page_num = request.GET.get('page', '1')
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    total_pages = 34
    if page_num < 1:
        page_num = 1
    elif page_num > total_pages:
        page_num = total_pages

    scanned_page = ScannedPanchangPage.objects.filter(page_number=page_num).first()
    all_pages = ScannedPanchangPage.objects.all().order_by('page_number')

    context = {
        'page_num': page_num,
        'total_pages': total_pages,
        'scanned_page': scanned_page,
        'all_pages': all_pages,
        'prev_page': page_num - 1 if page_num > 1 else None,
        'next_page': page_num + 1 if page_num < total_pages else None,
    }
    return render(request, 'mithila_panchang/scanned_panchang.html', context)


def download_ics(request, event_type, item_id):
    """Generate and return .ics calendar file."""
    if event_type == 'festival':
        item = get_object_or_404(Festival, pk=item_id)
        title = f"{item.title_hi} (मिथिला पाबनि)"
        desc = item.short_description
        start_date = item.date
    elif event_type == 'muhurat':
        item = get_object_or_404(MuhuratDate, pk=item_id)
        title = f"{item.category.name_hi} - {item.tithi_name} ({item.nakshatra_name})"
        desc = f"Mithila Panchang Muhurat Date. Month: {item.mithila_month_name}, Notes: {item.notes}"
        start_date = item.gregorian_date
    else:
        raise Http404("Invalid event type")

    ics_content = generate_ics_calendar_file(title, desc, start_date)
    response = HttpResponse(ics_content, content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="mithila_event_{start_date}.ics"'
    return response


@login_required
@user_passes_test(staff_check)
def admin_dashboard(request):
    """Custom Panchang Overview & Moderation Dashboard."""
    total_days = PanchangDay.objects.count()
    total_festivals = Festival.objects.count()
    total_muhurats = MuhuratDate.objects.count()
    needs_review_count = MuhuratDate.objects.filter(verification_status='NEEDS_REVIEW').count()
    verified_count = MuhuratDate.objects.filter(verification_status='VERIFIED').count()
    published_count = MuhuratDate.objects.filter(is_published=True).count()

    recent_muhurats = MuhuratDate.objects.all().order_by('-updated_at')[:15]
    audit_logs = PanchangAuditLog.objects.all().order_by('-timestamp')[:15]

    context = {
        'total_days': total_days,
        'total_festivals': total_festivals,
        'total_muhurats': total_muhurats,
        'needs_review_count': needs_review_count,
        'verified_count': verified_count,
        'published_count': published_count,
        'recent_muhurats': recent_muhurats,
        'audit_logs': audit_logs,
    }
    return render(request, 'mithila_panchang/admin_dashboard.html', context)


@login_required
@user_passes_test(staff_check)
def admin_verify_muhurat(request, pk):
    """Toggle verification / published state of a Muhurat date."""
    muhurat = get_object_or_404(MuhuratDate, pk=pk)
    action = request.POST.get('action')

    if action == 'verify':
        muhurat.verification_status = 'VERIFIED'
        muhurat.verified_by = request.user
        muhurat.verified_at = datetime.datetime.now()
        messages.success(request, f"Record #{muhurat.pk} marked as VERIFIED.")
    elif action == 'publish':
        muhurat.verification_status = 'PUBLISHED'
        muhurat.is_published = True
        messages.success(request, f"Record #{muhurat.pk} PUBLISHED.")
    elif action == 'unpublish':
        muhurat.is_published = False
        messages.warning(request, f"Record #{muhurat.pk} UNPUBLISHED.")

    muhurat.save()
    
    PanchangAuditLog.objects.create(
        record_type='MuhuratDate',
        record_id=muhurat.pk,
        action='VERIFY' if action == 'verify' else 'PUBLISH',
        changed_by=request.user,
        details=f"Admin updated state to {action}"
    )

    return redirect('mithila_panchang:admin_dashboard')


def mithila_songs_list(request):
    """Mithila Songs list view for /mithila-songs/"""
    songs = MithilaSong.objects.filter(is_published=True).order_by('order')
    
    # If no songs in DB yet, fallback list of initial 15 songs from prompt
    if not songs.exists():
        fallback_video_ids = [
            ("H501incNC74", "मिथिलाक पावन लोकगीत", "मैथिली संगीत"),
            ("5Jp7tGF6hbY", "मैथिली सोहर एवं विवाह गीत", "मिथिला कला"),
            ("R2l4yhQLHa4", "भगवती वंदना - मिथिला भजन", "मैथिली भक्ति"),
            ("JD9gsauGP4Y", "मधुश्रावणी व बटगवनी गीत", "पारम्परिक गीत"),
            ("jNOjTQfFyi8", "समदाओन - मैथिली विदाई गीत", "लोक संगीत"),
            ("uX-p-hfZH0c", "मिथिलाक पारम्परिक लोकगीत", "मैथिली सुर"),
            ("mbEfz3gsGFU", "जनकपुर धाम मैथिली गीत", "जनकपुर भक्ति"),
            ("anNyfBe9QTU", "मैथिली कजरी व झूमर", "पारम्परिक संगीत"),
            ("4pomVutNeZg", "मिथिला सांस्कृतिक लोकगीत", "मिथिला स्वर"),
            ("g8Iod6tadBg", "मैथिली सोहर संगीत", "सोहर मंगल"),
            ("bC3a5P9ZqNU", "सीता जन्म व विवाह गीत", "राम सीता गान"),
            ("DCaJ-2L2ro4", "मैथिली भगवती गीत संग्रह", "दुर्गा वंदना"),
            ("U6P-QuXm6Nw", "मिथिला की कोकिला संगीत", "शारदा सिन्हा स्वर"),
            ("8fikUVMIRCQ", "मैथिली लगन व समदाओन", "विवाह गान"),
            ("FPbQmReaM2Y", "मिथिलाक मधुर पारंपरिक गीत", "मैथिली विरासत"),
        ]
        songs = [
            {
                'video_id': vid,
                'title': title,
                'singer': singer,
                'thumbnail_url': f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            } for vid, title, singer in fallback_video_ids
        ]

    context = {
        'songs': songs,
    }
    return render(request, 'mithila_panchang/mithila_songs_list.html', context)

