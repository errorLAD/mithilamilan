from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import MithilaPride, MithilaPrideTimeline, MithilaPrideGallery
from .forms import MithilaPrideSubmissionForm

def person_list(request, forced_category=None):
    query = request.GET.get('q', '').strip()
    category = forced_category or request.GET.get('category', '').strip()
    location = request.GET.get('location', '').strip()
    era = request.GET.get('era', '').strip()

    persons_qs = MithilaPride.objects.filter(status__in=['approved', 'published'])

    if query:
        persons_qs = persons_qs.filter(
            Q(full_name__icontains=query) |
            Q(biography__icontains=query) |
            Q(contributions_to_mithila__icontains=query) |
            Q(place_location__icontains=query) |
            Q(publications_work__icontains=query) |
            Q(organization_institution__icontains=query)
        )

    if category:
        persons_qs = persons_qs.filter(category=category)

    if location:
        persons_qs = persons_qs.filter(place_location__icontains=location)

    if era:
        persons_qs = persons_qs.filter(era_generation=era)

    featured_persons = MithilaPride.objects.filter(status__in=['approved', 'published'], is_featured=True)[:4]

    paginator = Paginator(persons_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = MithilaPride.CATEGORY_CHOICES
    eras = MithilaPride.ERA_CHOICES

    section_title = "Mithila Pride & Scholars Directory"
    if category == 'scholar':
        section_title = "Notable Mithila Scholars & Academicians"
    elif category == 'artist':
        section_title = "Mithila Artists & Cultural Legends"
    elif category == 'writer':
        section_title = "Maithili Writers, Poets & Authors"

    context = {
        'persons': page_obj,
        'page_obj': page_obj,
        'featured_persons': featured_persons,
        'query': query,
        'category': category,
        'location': location,
        'era': era,
        'categories': categories,
        'eras': eras,
        'total_count': persons_qs.count(),
        'section_title': section_title,
    }
    return render(request, 'mithila_pride/person_list.html', context)

def person_detail(request, slug):
    person = get_object_or_404(MithilaPride, slug=slug)

    # Permission check for unapproved items
    if person.status not in ['approved', 'published']:
        if not (request.user.is_authenticated and (request.user.is_staff or request.user == person.submitted_by)):
            messages.warning(request, "This personality nomination is under admin review.")
            return redirect('mithila_pride:person_list')

    timeline = person.timeline_events.all().order_by('year_or_date')
    gallery = person.gallery_images.all()

    related_persons = MithilaPride.objects.filter(
        status__in=['approved', 'published']
    ).exclude(pk=person.pk).filter(
        Q(category=person.category) | Q(place_location__icontains=person.place_location.split(',')[0])
    )[:3]

    context = {
        'person': person,
        'timeline': timeline,
        'gallery': gallery,
        'related_persons': related_persons,
    }
    return render(request, 'mithila_pride/person_detail.html', context)

def person_submit(request):
    if request.method == 'POST':
        form = MithilaPrideSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)
            if request.user.is_authenticated:
                person.submitted_by = request.user
                if not person.submitter_name:
                    person.submitter_name = request.user.get_full_name() or request.user.username
                if not person.submitter_email:
                    person.submitter_email = request.user.email

            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                person.status = 'published'
                messages.success(request, f"Nomination for '{person.full_name}' published directly!")
            else:
                person.status = 'pending'
                messages.success(request, f"Thank you! Nomination for '{person.full_name}' submitted successfully. It will appear publicly after Admin approval.")
            
            person.save()
            return redirect(person.get_absolute_url() if person.status in ['approved', 'published'] else 'mithila_pride:person_list')
    else:
        form = MithilaPrideSubmissionForm()

    return render(request, 'mithila_pride/person_form.html', {'form': form})
