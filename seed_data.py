import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redditClone.settings')
django.setup()

from events.models import Event, EventScheduleDay, EventImportantDate
from pandits.models import PanditProfile
from mithila_pride.models import MithilaPride, MithilaPrideTimeline
from datetime import date

print("Seeding sample data...")

# 1. Seed Events & Festivals
event1, created = Event.objects.get_or_create(
    slug='durga-puja-2026-darbhanga',
    defaults={
        'title': 'Durga Puja 2026',
        'category': 'festival',
        'short_description': 'The most celebrated 5-day festival of Mithila featuring grand pandals, traditional Aarti, and cultural processions in Darbhanga.',
        'about': 'Durga Puja in Darbhanga is renowned across Bihar for its vibrant community spirit, traditional Maithili bhajan sandhyas, and exquisite idol craftsmanship. Thousands of devotees gather across central Darbhanga to offer prayers, celebrate cultural programs, and participate in evening aartis.',
        'history_background': 'Durga Puja in Mithila traces back centuries, combining Vedic rituals with classical Maithili music and community feasts. Historically supported by the Raj Darbhanga and local Samitis, it remains the spiritual high point of the year.',
        'start_date': date(2026, 10, 10),
        'end_date': date(2026, 10, 15),
        'location': 'Darbhanga, Bihar',
        'venue_info': 'Tower Chowk & Raj High School Ground, Darbhanga',
        'organizer': 'Central Durga Puja Samiti, Darbhanga',
        'contact_info': '+91 98765 11111 / contact@mithiladurgapuja.org',
        'map_location': 'https://maps.google.com/?q=Darbhanga+Tower+Chowk',
        'status': 'published',
        'is_featured': True,
    }
)

if created:
    EventScheduleDay.objects.create(
        event=event1,
        day_number=1,
        date=date(2026, 10, 10),
        title='Day 1 — 10 October (Maha Saptami)',
        morning_program='Navapatrika Snan & Kalparambha at 6:30 AM',
        afternoon_program='Pushpanjali & Bhog distribution at 1:00 PM',
        evening_program='Grand Sandhya Aarti & Maithili Cultural Song Night'
    )
    EventScheduleDay.objects.create(
        event=event1,
        day_number=2,
        date=date(2026, 10, 11),
        title='Day 2 — 11 October (Maha Ashtami)',
        morning_program='Special Ashtami Puja & Kumari Pujan at 8:00 AM',
        afternoon_program='Maha Prasad Distribution',
        evening_program='Dhunuchi Naach performance & Sandhi Puja preparation'
    )
    EventScheduleDay.objects.create(
        event=event1,
        day_number=3,
        date=date(2026, 10, 12),
        title='Day 3 — 12 October (Sandhi Puja & Navami)',
        morning_program='Maha Navami Havan & Chandi Path',
        afternoon_program='Community Feast (Bhandara)',
        evening_program='Classical Mithila Drama & Drama Performance'
    )
    EventScheduleDay.objects.create(
        event=event1,
        day_number=4,
        date=date(2026, 10, 13),
        title='Day 4 — 13 October (Vijaya Dashami)',
        morning_program='Dashami Puja & Sindoor Khela at 9:00 AM',
        afternoon_program='Preparation for Immersion Procession',
        evening_program='Grand Visarjan Procession to Bagmati River'
    )
    EventImportantDate.objects.create(
        event=event1,
        title='Sandhi Puja Muhurat',
        date_info='11 Oct, 11:42 PM - 12:30 AM',
        details='Peak auspicious timing for Ashtami-Navami transition'
    )

event2, created = Event.objects.get_or_create(
    slug='mithila-cultural-mahotsav-patna',
    defaults={
        'title': 'Mithila Cultural Mahotsav 2026',
        'category': 'cultural',
        'short_description': 'Annual celebration of Maithili literature, Madhubani art exhibitions, and traditional folk music.',
        'about': 'A 3-day extravaganza bringing together poets, Madhubani artists, folk singers, and culinary experts to highlight Mithila heritage in Bihar capital.',
        'start_date': date(2026, 11, 22),
        'end_date': date(2026, 11, 25),
        'location': 'Patna, Bihar',
        'venue_info': 'Bhartiya Nritya Kala Mandir, Patna',
        'organizer': 'Mithila Sanskriti Parishad',
        'contact_info': '+91 98765 22222',
        'status': 'published',
        'is_featured': True,
    }
)

# Pending Event for Moderation Queue
Event.objects.get_or_create(
    slug='local-vedic-chanting-competition',
    defaults={
        'title': 'State Level Vedic Chanting Competition',
        'category': 'educational',
        'short_description': 'Youth competition for Sanskrit Veda recitation and Vedic mathematics.',
        'about': 'Organized for high school and university students to encourage Sanskrit learning.',
        'start_date': date(2026, 12, 5),
        'end_date': date(2026, 12, 6),
        'location': 'Madhubani, Bihar',
        'organizer': 'Sanskrit Bhasha Samiti',
        'submitter_name': 'Rohan Sharma',
        'submitter_email': 'rohan@example.com',
        'status': 'pending',
    }
)

# 2. Seed Pandit & Astrologer Profiles
pandit1, created = PanditProfile.objects.get_or_create(
    slug='pandit-rameshwar-jha',
    defaults={
        'full_name': 'Pandit Rameshwar Jha',
        'profile_type': 'pandit',
        'designation': 'Senior Vedic Scholar & Karma Kanda Specialist',
        'whatsapp_number': '919876543210',
        'phone_number': '+91 98765 43210',
        'location': 'Darbhanga, Bihar & Delhi NCR',
        'address_area': 'Raj Parisar, Near Lakshmeshwar Temple, Darbhanga',
        'experience_years': 18,
        'languages': 'Maithili, Hindi, Sanskrit, English',
        'specialization': 'Griha Pravesh, Vivah Puja, Satyanarayan Katha, Vastu Shanti, Rudrabhishek',
        'services_offered': '• Complete Griha Pravesh Rituals & Vastu Puja\n• Vivah & Sagai Rituals\n• Rudrabhishek & Mahamrityunjaya Jaap\n• Satyanarayan Vrat Katha\n• Shanti Path & Hawan',
        'about': 'Pandit Rameshwar Jha belongs to a traditional Vedic family from Darbhanga. Trained at Kashi Vidya Parishad, Varanasi, he has conducted over 1,500 religious ceremonies with full Vedic authenticity and devotion.',
        'availability': 'Mon - Sun: 7:00 AM - 8:30 PM',
        'service_pricing': 'Griha Pravesh Puja: ₹3,100 | Rudrabhishek: ₹2,100 | Satyanarayan Katha: ₹1,100',
        'status': 'published',
        'is_verified': True,
        'is_featured': True,
    }
)

astro1, created = PanditProfile.objects.get_or_create(
    slug='astrologer-priya-sharma',
    defaults={
        'full_name': 'Dr. Priya Sharma (Jyotish Acharya)',
        'profile_type': 'astrologer',
        'designation': 'Vedic Astrologer, Kundali Reader & Vastu Consultant',
        'whatsapp_number': '919876543211',
        'phone_number': '+91 98765 43211',
        'location': 'Delhi NCR & Madhubani',
        'address_area': 'Sector 62, Noida & Madhubani Town',
        'experience_years': 14,
        'languages': 'Hindi, English, Maithili',
        'specialization': 'Janam Kundali Reading, Match Making, Career Guidance, Prashna Kundali, Gemstone Advice',
        'services_offered': '• In-depth Horoscope Analysis & Chart Matching\n• Business & Career Horoscope Predictions\n• Vastu Shastra Consultation for Homes & Offices\n• Gemstone & Rudraksha Recommendation',
        'about': 'Gold Medalist Jyotish Acharya with 14+ years of practice in Parashari astrology. Specializes in accurate life event forecasting, marriage compatibility analysis, and practical remedies.',
        'availability': 'Mon - Sat: 10:00 AM - 7:00 PM',
        'service_pricing': 'Full Kundali Analysis (45 Mins): ₹1,100 | Kundali Matching: ₹750',
        'status': 'published',
        'is_verified': True,
        'is_featured': True,
    }
)

# Pending Pandit profile for Moderation Queue
PanditProfile.objects.get_or_create(
    slug='pandit-vidyadhar-mishra',
    defaults={
        'full_name': 'Pandit Vidyadhar Mishra',
        'profile_type': 'both',
        'designation': 'Vedic Karma Kanda & Prashna Kundali Specialist',
        'whatsapp_number': '919876543212',
        'location': 'Patna, Bihar',
        'experience_years': 10,
        'languages': 'Maithili, Hindi',
        'specialization': 'Navgrah Shanti, Vastu, Vivah Puja',
        'services_offered': 'Pujas, Kundali Reading',
        'about': 'Experienced priest providing authentic Vedic services across Bihar.',
        'status': 'pending',
    }
)

# 3. Seed Mithila Pride & Scholars
scholar1, created = MithilaPride.objects.get_or_create(
    slug='scholar-dr-kameshwar-singh',
    defaults={
        'full_name': 'Dr. Kameshwar Singh',
        'category': 'scholar',
        'era_generation': '20th_century',
        'place_location': 'Darbhanga, Bihar',
        'biography': 'Maharaja Dr. Kameshwar Singh of Darbhanga was a visionary scholar, philanthropist, and patron of higher education who founded Kameshwar Singh Darbhanga Sanskrit University and donated extensive land and libraries for modern education.',
        'early_life': 'Born into the royal house of Darbhanga Raj, he was tutored in traditional Sanskrit literature as well as western political science and economics.',
        'education': 'D.Litt. (Hon.), Patron of Banaras Hindu University (BHU) and Patna University.',
        'career': 'President of All India Landholders Association, Member of Constituent Assembly of India, and Founder Chancellor of Sanskrit University.',
        'major_achievements': 'Donated Anand Bagh Palace and thousands of ancient palm-leaf manuscripts to establish K.S.D. Sanskrit University.',
        'awards': 'Knight Commander of the Order of the Indian Empire (KCIE), Doctor of Letters honoris causa.',
        'publications_work': 'Monographs on Sanskrit preservation, Vedic education policy papers, and patrons of Maithili literature.',
        'contributions_to_mithila': 'Pioneered higher university education in Bihar and established Darbhanga as a globally recognized center for Sanskrit and Maithili research.',
        'organization_institution': 'K.S.D. Sanskrit University & L.N. Mithila University',
        'website_social_links': 'https://en.wikipedia.org/wiki/Kameshwar_Singh',
        'status': 'published',
        'is_featured': True,
    }
)

if created:
    MithilaPrideTimeline.objects.create(
        person=scholar1,
        year_or_date='1907',
        title='Birth at Darbhanga Palace',
        description='Born into the historic royal lineage of Mithila'
    )
    MithilaPrideTimeline.objects.create(
        person=scholar1,
        year_or_date='1960',
        title='Establishment of KSD Sanskrit University',
        description='Donated palace grounds and royal manuscript library to create India\'s premier Sanskrit University'
    )

scholar2, created = MithilaPride.objects.get_or_create(
    slug='scholar-mahakavi-vidyapati',
    defaults={
        'full_name': 'Mahakavi Vidyapati Thakur',
        'category': 'writer',
        'era_generation': 'classical',
        'place_location': 'Bisaul / Bisi, Madhubani, Bihar',
        'biography': 'Vidyapati (c. 1352 – c. 1448) is the immortal classical poet, polymath, and saint of Mithila known as Abhinava Jayadeva. His devotional songs dedicated to Lord Shiva (Nachari) and Radha-Krishna immortalized Maithili language across Eastern India.',
        'early_life': 'Born in Bisaul village of Madhubani into a distinguished family of scholars.',
        'career': 'Court poet and minister to King Shiva Singh and Queen Lakhima Devi of Oiniwar dynasty.',
        'major_achievements': 'Authored Kirtilata, Kirtipataka, Purusha Pariksha, and thousands of Maithili Padavali lyrics.',
        'contributions_to_mithila': 'Laid the bedrock of Maithili written literature and spiritual song traditions across Mithila, Bengal, and Assam.',
        'status': 'published',
        'is_featured': True,
    }
)

# Pending Nomination for Moderation Queue
MithilaPride.objects.get_or_create(
    slug='scholar-prof-anand-kumar',
    defaults={
        'full_name': 'Prof. Anand Kumar',
        'category': 'researcher',
        'era_generation': 'contemporary',
        'place_location': 'Patna / Samastipur',
        'biography': 'Renowned mathematician and educator dedicated to empowering underprivileged students from Bihar.',
        'contributions_to_mithila': 'Mentored hundreds of rural students into premiere engineering institutions.',
        'submitter_name': 'Amit Sen',
        'submitter_email': 'amit@example.com',
        'status': 'pending',
    }
)

print("Sample data successfully seeded!")
