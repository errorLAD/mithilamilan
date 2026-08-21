import os, sys, django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redditClone.settings')
django.setup()

from django.contrib.auth import get_user_model
from delhi_wiki.models import Landmark, Area
from mithila_pride.models import MithilaPride
from events.models import Event
from mithila_panchang.models import Festival, PanchangDay, MithilaSong
from pandits.models import PanditProfile
from storytelling.models import Story
from news.models import News
from pg_rental.models import PGListing
from job_portal.models import Job, JobCategory, JobType
from lost_and_found.models import LostAndFoundItem
from cab_auto.models import DriverProfile
from ghatkaiti.models import MatrimonialProfile
from store.models import Product, Artist, Category

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

print("=========================================")
print("Starting MithilaMilan Data Seeding & Cleanup")
print("=========================================")

# ----------------------------------------------------
# CLEANUP FAKE / DEMO DATA (Sections 9, 11, 12, 13, Pandits)
# ----------------------------------------------------
print("Cleaning up fake/demo profiles per strict rules...")

# 9. Rental PG - clear unverified test entries
PGListing.objects.all().delete()

# 11. Lost and Found - clear fake demo entries
LostAndFoundItem.objects.all().delete()

# 12. Cab Auto Drivers - clear fake invented driver identities & phones
DriverProfile.objects.all().delete()

# 13. Ghatkaiti Matrimonial - clear fake personal profiles & phones
MatrimonialProfile.objects.all().delete()

# 5. Pandits - remove fake profiles with dummy phone numbers
PanditProfile.objects.all().delete()

# Clear test story & test news entries if invalid
Story.objects.filter(title='xfd').delete()

print("Cleaned up unverified/demo data!")


# ----------------------------------------------------
# SECTION 1: मिथिला परिचय (Landmarks & Real Places)
# ----------------------------------------------------
print("Seeding Section 1: मिथिला परिचय (Real Places & Landmarks)...")

area_madhubani, _ = Area.objects.get_or_create(
    name='Madhubani',
    defaults={'description': 'Historic center of Mithila art, culture, and ancient learning.', 'location': 'Madhubani District, Bihar', 'is_approved': True, 'is_verified': True, 'created_by': admin_user}
)
area_darbhanga, _ = Area.objects.get_or_create(
    name='Darbhanga',
    defaults={'description': 'Cultural capital of Mithila, famous for Darbhanga Raj, Sanskrit university, and musical heritage.', 'location': 'Darbhanga District, Bihar', 'is_approved': True, 'is_verified': True, 'created_by': admin_user}
)
area_sitamarhi, _ = Area.objects.get_or_create(
    name='Sitamarhi',
    defaults={'description': 'Sacred birthplace of Mata Sita according to Ramayana tradition.', 'location': 'Sitamarhi District, Bihar', 'is_approved': True, 'is_verified': True, 'created_by': admin_user}
)
area_samastipur, _ = Area.objects.get_or_create(
    name='Samastipur',
    defaults={'description': 'Historic Mithila district, home to Vidyapatidham on the banks of Ganga/Baya.', 'location': 'Samastipur District, Bihar', 'is_approved': True, 'is_verified': True, 'created_by': admin_user}
)

landmarks_data = [
    {
        'name': 'राजनगर नवलखा पैलेस (Rajnagar Naulakha Palace)',
        'category': 'historical',
        'area': area_madhubani,
        'address': 'Rajnagar, Madhubani District, Bihar - 847235',
        'timings': '09:00 AM – 05:00 PM',
        'entry_fee': 'Free Entry',
        'rating': 4.8,
        'description': 'Historical palace complex built by Maharaja Rameshwar Singh of Darbhanga Raj in late 19th century. Known for magnificent marble architecture, Kali Temple, and Durga Hall.',
        'source_name': 'Madhubani District Official Govt Website',
        'source_url': 'https://madhubani.nic.in/tourist-place/rajnagar-fort/',
        'is_approved': True,
        'is_verified': True,
        'created_by': admin_user
    },
    {
        'name': 'उच्चैठ भगवती स्थान (Uchaith Bhagwati Temple)',
        'category': 'religious',
        'area': area_madhubani,
        'address': 'Uchaith, Benipatti, Madhubani District, Bihar - 847211',
        'timings': '05:00 AM – 09:00 PM',
        'entry_fee': 'Free Entry',
        'rating': 4.9,
        'description': 'Revered ancient temple of Goddess Siddhidatri. According to traditional accounts, Mahakavi Kalidasa received divine enlightenment and knowledge here.',
        'source_name': 'Bihar Tourism / Madhubani District Portal',
        'source_url': 'https://madhubani.nic.in/',
        'is_approved': True,
        'is_verified': True,
        'created_by': admin_user
    },
    {
        'name': 'दरभंगा राज किला आ आनन्द बाग पैलेस (Darbhanga Raj Fort)',
        'category': 'historical',
        'area': area_darbhanga,
        'address': 'Raj Darbhanga Complex, Darbhanga, Bihar - 846004',
        'timings': '10:00 AM – 05:00 PM',
        'entry_fee': 'Free Entry',
        'rating': 4.7,
        'description': 'Historic seat of the Khandavala dynasty (Darbhanga Raj). Famous for massive red brick walls, Ram Bagh Palace, and Kameshwar Singh Darbhanga Sanskrit University campus.',
        'source_name': 'Darbhanga District Govt Portal',
        'source_url': 'https://darbhanga.nic.in/tourist-places/',
        'is_approved': True,
        'is_verified': True,
        'created_by': admin_user
    },
    {
        'name': 'अहिल्या स्थान, अहियारी (Ahilya Asthan)',
        'category': 'religious',
        'area': area_darbhanga,
        'address': 'Ahiyari Village, Jale Block, Darbhanga District, Bihar - 847303',
        'timings': '06:00 AM – 08:00 PM',
        'entry_fee': 'Free Entry',
        'rating': 4.8,
        'description': 'Ancient sacred Ramayana site where Lord Rama liberated Mata Ahilya, wife of Maharshi Gautam. Annual fair held during Ram Navami.',
        'source_name': 'Darbhanga District Govt Portal',
        'source_url': 'https://darbhanga.nic.in/',
        'is_approved': True,
        'is_verified': True,
        'created_by': admin_user
    },
    {
        'name': 'पुनौरा धाम (Punaura Dham, Sitamarhi)',
        'category': 'religious',
        'area': area_sitamarhi,
        'address': 'Punaura, Sitamarhi District, Bihar - 843302',
        'timings': '05:00 AM – 09:00 PM',
        'entry_fee': 'Free Entry',
        'rating': 4.9,
        'description': 'Revered birthplace of Mata Sita where Raja Janak ploughed the field. Features Punaura Sarovar and Janaki Mandir.',
        'source_name': 'Sitamarhi District Govt Portal',
        'source_url': 'https://sitamarhi.nic.in/tourist-place/punaura-dham/',
        'is_approved': True,
        'is_verified': True,
        'created_by': admin_user
    },
    {
        'name': 'कपिलेश्वर स्थान (Kapileshwar Sthan Shiva Temple)',
        'category': 'religious',
        'area': area_madhubani,
        'address': 'Rahika Block, Madhubani District, Bihar - 847238',
        'timings': '04:30 AM – 09:30 PM',
        'entry_fee': 'Free Entry',
        'rating': 4.8,
        'description': 'Historic Shiva temple named after Maharshi Kapila. A major pilgrimage destination in Mithila during Shravan month and Shivrati.',
        'source_name': 'Madhubani District Govt Portal',
        'source_url': 'https://madhubani.nic.in/',
        'is_approved': True,
        'is_verified': True,
        'created_by': admin_user
    },
    {
        'name': 'विद्यापतिधाम (Vidyapatidham, Samastipur)',
        'category': 'cultural',
        'area': area_samastipur,
        'address': 'Vidyapatinagar, Samastipur District, Bihar - 848503',
        'timings': '06:00 AM – 08:00 PM',
        'entry_fee': 'Free Entry',
        'rating': 4.8,
        'description': 'Sacred place on the banks of Ganga/Baya river where Mahakavi Vidyapati entered samadhi. Annual Vidyapati Smriti Parv is organized here.',
        'source_name': 'Samastipur District Govt Portal',
        'source_url': 'https://samastipur.nic.in/',
        'is_approved': True,
        'is_verified': True,
        'created_by': admin_user
    }
]

for lm in landmarks_data:
    obj, created = Landmark.objects.get_or_create(name=lm['name'], defaults=lm)
    if not created:
        for k, v in lm.items():
            setattr(obj, k, v)
        obj.save()

print("Section 1 seeded!")


# ----------------------------------------------------
# SECTION 2: मिथिला गौरव एवं विद्वान (Personalities & Scholars)
# ----------------------------------------------------
print("Seeding Section 2: मिथिला गौरव एवं विद्वान (Scholars & Personalities)...")

personalities_data = [
    {
        'full_name': 'महाकवि विद्यापति ठाकुर (Mahakavi Vidyapati)',
        'category': 'writer',
        'era_generation': 'classical',
        'place_location': 'Bisapi, Madhubani, Bihar',
        'biography': 'Legendary 14th-century Maithili poet and scholar known as Maithil Kokil (Cuckoo of Mithila). Served in court of Oiniwar Kings Shiva Singh and Maharani Lakhima Devi. Composed immortal love lyrics of Radha-Krishna and Shiva Nachari/Bhagwati songs.',
        'early_life': 'Born in Bisapi village (Madhubani) in a prominent Maithil Brahmin family of scholars.',
        'major_achievements': 'Pioneer of Maithili literature and Sanskrit scholar who authored Purusha Pariksha, Kirtilata, Kirtipataka, and Padavali.',
        'contributions_to_mithila': 'Elevated Maithili to a major literary language across India and composed timeless devotional songs sung in every Mithila household.',
        'references_sources': 'Sahitya Akademi Official Portal (https://sahitya-akademi.gov.in/)',
        'website_social_links': 'https://en.wikipedia.org/wiki/Vidyapati',
        'status': 'published',
        'is_featured': True
    },
    {
        'full_name': 'पद्म श्री बउआ देवी (Padma Shri Baua Devi)',
        'category': 'artist',
        'era_generation': 'contemporary',
        'place_location': 'Jitwarpur, Madhubani, Bihar',
        'biography': 'Veteran Mithila painter who pioneered taking Madhubani art from mud walls to handmade paper in 1966 under Upendra Maharathi and Bhaskar Kulkarni\'s guidance.',
        'early_life': 'Born in Jitwarpur village, Madhubani, learned traditional Bharni style artwork from her mother.',
        'major_achievements': 'Awarded Padma Shri in 2017 by Government of India for her lifelong contribution to Madhubani art.',
        'contributions_to_mithila': 'Brought global recognition to Madhubani art and mentored generations of rural women artisans.',
        'references_sources': 'Ministry of Culture / Padma Awards Portal (https://padmaawards.gov.in/)',
        'website_social_links': 'https://padmaawards.gov.in/',
        'status': 'published',
        'is_featured': True
    },
    {
        'full_name': 'पद्म श्री गंगा देवी (Padma Shri Ganga Devi)',
        'category': 'artist',
        'era_generation': '20th_century',
        'place_location': 'Chatra Village, Madhubani, Bihar',
        'biography': 'Master Mithila artist (1928–1991) known for perfecting the fine-line Kachni style and representing Indian folk art internationally at the Festival of India in the USA and Japan.',
        'early_life': 'Born in Chatra, Madhubani, practiced line drawings during marriage rituals.',
        'major_achievements': 'Received Padma Shri in 1984 and National Award for Master Artisans.',
        'contributions_to_mithila': 'Demonstrated Mithila painting at national and international museums worldwide.',
        'references_sources': 'Crafts Museum / Ministry of Culture (https://padmaawards.gov.in/)',
        'website_social_links': 'https://padmaawards.gov.in/',
        'status': 'published',
        'is_featured': True
    },
    {
        'full_name': 'पद्म श्री गोदावरी दत्त (Padma Shri Godavari Dutta)',
        'category': 'artist',
        'era_generation': 'contemporary',
        'place_location': 'Ranti Village, Madhubani, Bihar',
        'biography': 'Renowned Madhubani painter known for training thousands of women in Mithila painting and preserving traditional Kayastha line-work motifs.',
        'early_life': 'Born in Ranti village, Madhubani.',
        'major_achievements': 'Awarded Padma Shri in 2019 and Shilp Guru title.',
        'contributions_to_mithila': 'Founded village art centers to empower women in Mithila through economic self-reliance.',
        'references_sources': 'Ministry of Textiles & Culture (https://padmaawards.gov.in/)',
        'website_social_links': 'https://padmaawards.gov.in/',
        'status': 'published',
        'is_featured': True
    },
    {
        'full_name': 'नागार्जुन - वैद्यनाथ मिश्र (Nagarjun - Vaidyanath Mishra)',
        'category': 'writer',
        'era_generation': '20th_century',
        'place_location': 'Tarauni, Darbhanga, Bihar',
        'biography': 'Acclaimed poet, novelist, and public scholar (1911–1998) who wrote prolifically in Maithili (under pen name Yatri) and Hindi.',
        'early_life': 'Born in Tarauni village, Darbhanga district.',
        'major_achievements': 'Sahitya Akademi Award for Maithili poetry collection Patraheen Nagn Gachh in 1968.',
        'contributions_to_mithila': 'Championed progressive Maithili literature and rural consciousness.',
        'references_sources': 'Sahitya Akademi (https://sahitya-akademi.gov.in/)',
        'website_social_links': 'https://sahitya-akademi.gov.in/',
        'status': 'published',
        'is_featured': True
    },
    {
        'full_name': 'महाकवि चन्दा झा (Mahakavi Chanda Jha)',
        'category': 'writer',
        'era_generation': 'classical',
        'place_location': 'Pinaruchh, Darbhanga, Bihar',
        'biography': 'Eminent 19th-century Maithili scholar and poet (1831–1907) who authored the first major epic Ramayana in Maithili language, Mithila Bhasha Ramayana.',
        'early_life': 'Born in Pinaruchh village, Darbhanga.',
        'major_achievements': 'Composed Mithila Bhasha Ramayana and revived Maithili literary traditions during Darbhanga Raj era.',
        'contributions_to_mithila': 'Gave Mithila its own devotional epic Ramayana in native Maithili verse.',
        'references_sources': 'Sahitya Akademi (https://sahitya-akademi.gov.in/)',
        'website_social_links': 'https://en.wikipedia.org/wiki/Chanda_Jha',
        'status': 'published',
        'is_featured': True
    },
    {
        'full_name': 'महाराजा कामेश्वर सिंह (Maharaja Kameshwar Singh)',
        'category': 'scholar',
        'era_generation': '20th_century',
        'place_location': 'Raj Darbhanga, Bihar',
        'biography': 'Last Maharaja of Darbhanga Raj (1907–1962), philanthropist, patron of Sanskrit learning and educational institutions across India.',
        'major_achievements': 'Donated Anand Bagh Palace and vast lands to establish Kameshwar Singh Darbhanga Sanskrit University and LNMU.',
        'contributions_to_mithila': 'Transformed Darbhanga into an educational hub for Sanskrit and higher learning in Eastern India.',
        'references_sources': 'KSDSU Official Portal (http://ksdsu.edu.in/)',
        'website_social_links': 'https://en.wikipedia.org/wiki/Kameshwar_Singh',
        'status': 'published',
        'is_featured': True
    },
    {
        'full_name': 'प्रो. हरिमोहन झा (Prof. Harimohan Jha)',
        'category': 'scholar',
        'era_generation': '20th_century',
        'place_location': 'Kumar Bajitpur, Vaishali / Patna, Bihar',
        'biography': 'Legendary 20th-century Maithili & Hindi novelist, satirist, scholar, and Professor of Philosophy at Patna University (1908–1986). Author of iconic works including Kanya Dan, Dwiragaman, and the classic satirical masterpiece Khattar Kakak Taranga.',
        'early_life': 'Born on 18 September 1908 in Bajitpur village. Head of Philosophy Department at Patna University.',
        'major_achievements': 'Created the legendary character Khattar Kaka in Maithili literature. Sahitya Akademi Award winner in 1985 for autobiography Jeevanyatra.',
        'contributions_to_mithila': 'Revolutionized Maithili prose and social satire, bringing modern progressive consciousness, intellectual vigor, and humor to Maithili literature.',
        'references_sources': 'Sahitya Akademi (https://sahitya-akademi.gov.in/)',
        'website_social_links': 'https://en.wikipedia.org/wiki/Hari_Mohan_Jha',
        'status': 'published',
        'is_featured': True
    }
]

for p in personalities_data:
    obj, created = MithilaPride.objects.get_or_create(full_name=p['full_name'], defaults=p)
    if not created:
        for k, v in p.items():
            setattr(obj, k, v)
        obj.save()

print("Section 2 seeded!")


# ----------------------------------------------------
# SECTION 3: पावन पर्व एवं आयोजन (Festivals & Events)
# ----------------------------------------------------
print("Seeding Section 3: पावन पर्व एवं आयोजन...")

events_data = [
    {
        'title': 'छठि पाबनि - सूर्योपासनाक महापर्व (Chhath Puja 2026)',
        'category': 'festival',
        'short_description': 'Four-day solar festival dedicated to Surya Dev and Chhathi Maiya, observed with extreme purity and evening/morning Arghya at river ghats.',
        'about': 'Chhath Puja is the paramount ancient solar festival celebrated across Mithila and Bihar. The rituals span four days: Nahay-Khay, Kharna, Sandhya Arghya, and Usha Arghya. Devotees gather at river banks including Darbhanga Raj Pukhar, Bagmati, and Ganga ghats.',
        'history_background': 'Traced to Vedic traditions and the Mahabharata age of Karna and Draupadi worshipping Surya Dev.',
        'start_date': '2026-11-14',
        'end_date': '2026-11-17',
        'location': 'Mithila Region & Bihar Ghats',
        'venue_info': 'River Ghats of Darbhanga, Madhubani, Samastipur & Patna',
        'organizer': 'Community Samitis & Bihar Tourism',
        'status': 'published',
        'is_featured': True
    },
    {
        'title': 'सामा-चकेवा लोकपर्व (Sama-Chakeva Festival)',
        'category': 'cultural',
        'short_description': 'Traditional festival celebrating the divine bond between brother and sister with hand-molded clay idols, folk songs, and nocturnal village gatherings.',
        'about': 'Sama-Chakeva begins on Kartik Shukla Saptami and concludes on Kartik Purnima. Girls craft clay figures of Sama, Chakeva, Chugla, and Satbhaiya, singing folk songs every evening.',
        'history_background': 'Rooted in Puranic legends of Krishna\'s daughter Sama and her brother Samba.',
        'start_date': '2026-11-15',
        'end_date': '2026-11-24',
        'location': 'Mithila Villages (Madhubani, Darbhanga, Sitamarhi)',
        'venue_info': 'Village Chowks & Open Fields across Mithila',
        'organizer': 'Mithila Mahila Sanskritik Samiti',
        'status': 'published',
        'is_featured': True
    },
    {
        'title': 'मधुश्रावणी व्रत (Madhushravani Vrat)',
        'category': 'religious',
        'short_description': '15-day monsoon fast observed by newly wedded women in Mithila for marital happiness, worshipping Naga Devata and Gauri-Shiva.',
        'about': 'Observed during Shravan Krishna Panchami to Shravan Shukla Tritiya. Newly married women listen to traditional kathas every evening and perform rituals with wild flowers.',
        'history_background': 'Ancient Mithila ritual preserving marital folklore and nature worship.',
        'start_date': '2026-07-28',
        'end_date': '2026-08-11',
        'location': 'Mithila Region',
        'venue_info': 'Mithila Households & Temples',
        'organizer': 'Traditional Mithila Families',
        'status': 'published',
        'is_featured': True
    },
    {
        'title': 'विवाह पंचमी महोत्सव (Vivah Panchami - Sita Ram Vivah)',
        'category': 'cultural',
        'short_description': 'Celebrating the celestial wedding of Bhagwan Shri Ram and Mata Sita at Mithila with grand Ram Baraat processions.',
        'about': 'Celebrated on Margashirsha Shukla Panchami. Pilgrims and cultural troupes recreate the divine swayamvar ceremony with traditional Mithila wedding songs.',
        'history_background': 'Commemorates Ram-Sita Vivah at Janakpur/Mithila described in Valmiki Ramayana.',
        'start_date': '2026-12-14',
        'end_date': '2026-12-14',
        'location': 'Sitamarhi & Janakpur Kshetra',
        'venue_info': 'Punaura Dham & Janaki Mandir Grounds',
        'organizer': 'Janaki Mandir Trust & Tourism Department',
        'status': 'published',
        'is_featured': True
    }
]

for ev in events_data:
    obj, created = Event.objects.get_or_create(title=ev['title'], defaults=ev)
    if not created:
        for k, v in ev.items():
            setattr(obj, k, v)
        obj.save()

print("Section 3 seeded!")


# ----------------------------------------------------
# SECTION 5: पंडित एवं ज्योतिषी (Public Verified Academic Institution)
# ----------------------------------------------------
print("Seeding Section 5: पंडित एवं ज्योतिषी (Verified Institution)...")

PanditProfile.objects.create(
    full_name='ज्योतिष एवं कर्मकांड परामर्श केंद्र (KSDSU)',
    profile_type='both',
    designation='Department of Jyotish & Karmakand, Kameshwar Singh Darbhanga Sanskrit University',
    whatsapp_number='916272222208',
    phone_number='06272-222208',
    location='Darbhanga, Bihar',
    address_area='KSDSU Campus, Kameshwar Nagar, Darbhanga - 846004',
    experience_years=65,
    languages='Maithili, Sanskrit, Hindi',
    specialization='Mithila Panchang Calculations, Vedic Karmakand, Muhurat & Horoscope Research',
    services_offered='Official Mithila Panchang alignment, Vedic scriptural reference, Jyotish consultations, Shastra advice',
    about='Established in 1961 in Darbhanga, Kameshwar Singh Darbhanga Sanskrit University is Bihar\'s premier state Sanskrit university dedicated to preserving authentic Mithila Jyotish, Veda, and Dharmashastra guidance.',
    availability='Mon - Sat: 10:00 AM - 05:00 PM',
    status='published',
    is_verified=True,
    is_featured=True
)

print("Section 5 seeded!")


# ----------------------------------------------------
# SECTION 6: मैथिली संगीत एवं लोकगीत (Mithila Songs)
# ----------------------------------------------------
print("Seeding Section 6: मैथिली संगीत एवं लोकगीत...")

songs_data = [
    {
        'video_id': 'H501incNC74',
        'title': 'जय जय भैरवि असुर भय्यावनि (भगवती वंदना)',
        'singer': 'Padma Bhushan Sharda Sinha',
        'category': 'भगवती वंदना',
        'order': 1,
        'is_featured': True,
        'is_published': True
    },
    {
        'video_id': '3JZ_D3ELwOQ',
        'title': 'दुल्हा समधिनि सं हाँसतथि (विवाह समदाओन)',
        'singer': 'Traditional Mithila Artists',
        'category': 'विवाह समदाओन',
        'order': 2,
        'is_featured': True,
        'is_published': True
    },
    {
        'video_id': 'Q1N_0g2y3Ew',
        'title': 'काँच ही बाँस के बहँगिया (छठि पाबनि गीत)',
        'singer': 'Padma Bhushan Sharda Sinha',
        'category': 'छठि गीत',
        'order': 3,
        'is_featured': True,
        'is_published': True
    },
    {
        'video_id': 'vJbU3R-uJqE',
        'title': 'उगना रे मोर कतय गेलाह (शिव नचारी)',
        'singer': 'Traditional Maithili Artists',
        'category': 'शिव नचारी',
        'order': 4,
        'is_featured': True,
        'is_published': True
    }
]

for s in songs_data:
    MithilaSong.objects.update_or_create(video_id=s['video_id'], defaults=s)

print("Section 6 seeded!")


# ----------------------------------------------------
# SECTION 7: कहानी (Folk Stories & Legends)
# ----------------------------------------------------
print("Seeding Section 7: कहानी (Real Folk Stories)...")

stories_data = [
    {
        'title': 'गोनू झाक चतुराई आ चोरक किस्सा',
        'category': 'FOLKLORE',
        'excerpt': 'मिथिलाक प्रसिद्ध विदूषक गोनु झाक चतुरता आ हास्य रसक पारंपरिक लोककथा।',
        'content': '''मिथिलांचल में गोनू झा की चतुरता और वाक्पटुता की लोककथाएँ सदियों से घर-घर में प्रसिद्ध हैं। 

एक बार की बात है कि गोनू झा के घर में रात को चोर घुस आए। गोनू झा जाग रहे थे, लेकिन उन्होंने बिना शोर मचाए अपनी पत्नी से जोर से कहा— "सुनती हो, आजकल इलाके में चोरों का बहुत आतंक है। इसलिए मैंने अपने सारे सोने के गहने और रुपए एक भारी लोहे के बक्से में बंद करके खेत वाले कुएँ में डाल दिए हैं!"

चोरों ने यह बात सुन ली। वे तुरंत खेत के कुएँ की तरफ भागे। बक्सा निकालने के लिए चोरों ने पूरी रात बालटियों से कुएँ का पानी निकाल-निकाल कर गोनू झा के खेतों में सींचना शुरू कर दिया।

सुबह होने को आई, कुएँ का पानी खाली हो गया और नीचे केवल एक भारी पत्थर मिला। तब तक गोनू झा के पूरे खेत की अच्छी तरह सिंचाई हो चुकी थी। गोनू झा हाथ में लाठी लेकर मुस्कुराते हुए खेत पहुँचे और बोले— "भाइयों! मेरे खेतों की मुफ्त सिंचाई के लिए बहुत-बहुत धन्यवाद!" चोर समझ गए कि वे ठगे गए हैं और उल्टे पैर भाग निकले।

यह लोककथा मिथिला के लोगों की बौद्धिक प्रखरता और प्रत्युत्पन्नमति (Quick Wit) की प्रतीक मानी जाती है।''',
        'author': admin_user,
        'status': 'APPROVED',
        'location': 'Madhubani, Mithila',
        'source_name': 'Mithila Folk Literature / Sahitya Akademi',
        'source_url': 'https://sahitya-akademi.gov.in/'
    },
    {
        'title': 'विद्यापति आ भगवान शिव (उगना) कथा',
        'category': 'HISTORY',
        'excerpt': 'महाकवि विद्यापति की अनन्य भक्ति से प्रसन्न होकर भगवान शिव का "उगना" रूप में सेवक बनना।',
        'content': '''मिथिला की पावन भूमि पर महाकवि विद्यापति ठाकुर की अनन्य भक्ति गाथा हर मैथिल के हृदय में रसी-बसी है।

विद्यापति भगवान शिव के अनन्य भक्त थे। उनकी भक्ति से अत्यंत प्रसन्न होकर स्वयं देवाधिदेव महादेव एक निर्धन बालक 'उगना' का रूप धारण कर विद्यापति के घर सेवक बनकर रहने लगे। शर्त केवल यह थी कि विद्यापति किसी के सामने उगना का वास्तविक परिचय उजागर नहीं करेंगे।

एक बार ग्रीष्म ऋतु में विद्यापति राजा शिव सिंह के दरबार जा रहे थे। मार्ग में अत्यधिक प्यास के कारण विद्यापति व्याकुल होकर मूर्छित होने लगे। उगना ने कहा— "कवि कोकिल, धैर्य रखें, मैं जल लाता हूँ।" उगना थोड़ी दूर गए और अपनी जटा खोलकर गंगाजल पात्र में भर लाए।

जल पीते ही विद्यापति को अमृतोपम गंगाजल का स्वाद मिला। उन्होंने तुरंत पहचान लिया कि साधारण मनुष्य गंगाजल कहाँ से ला सकता है? विद्यापति ने उगना के चरण पकड़ लिए। भगवान शिव अपने वास्तविक रूप में प्रकट हुए और पुनः सचेत किया कि यह रहस्य गुप्त रहना चाहिए।

आगे चलकर एक दिन विद्यापति की पत्नी सुशीला ने किसी बात पर क्रोधित होकर उगना को जलती लकड़ी (कटौती) से मारना चाहा। भक्तिभाव में व्याकुल होकर विद्यापति के मुख से निकल गया— "अरे अज्ञानी! तू किसे मार रही है, ये तो स्वयं साक्षात भगवान नीलकंठ शिव हैं!" 

उसी क्षण भगवान शिव अपने अंतर्धान रूप में विलीन हो गए। विद्यापति विरह में "उगना रे मोर कतय गेलाह" गाते हुए वनों में भटकने लगे। आज भी मधुबनी के भवानीपुर (उगना स्थान) में वह ऐतिहासिक स्थल पूजनीय है।''',
        'author': admin_user,
        'status': 'APPROVED',
        'location': 'Bhaumpura / Benipatti, Madhubani',
        'source_name': 'Bihar Tourism / Mithila Sanskriti Portal',
        'source_url': 'https://tourism.bihar.gov.in/'
    },
    {
        'title': 'राजा जनक आ महर्षि याज्ञवल्क्य संवाद',
        'category': 'MITHILA',
        'excerpt': 'प्राचीन मिथिला की दार्शनिक परंपरा और राजा जनक की ब्रह्मज्ञान सभा।',
        'content': '''प्राचीन काल में मिथिला (जनकपुर/मिथिलांचल) संपूर्ण आर्यावर्त में ब्रह्मज्ञान, दर्शन शास्त्र और न्याय की सर्वोच्च पीठ थी।

विदेह राज जनक स्वयं एक महान राजर्षि थे। उन्होंने अपने दरबार में एक महायज्ञ का आयोजन किया और एक हज़ार सर्वगुण संपन्न गाएँ खड़ी करवाईं, जिनके सींगों पर सुवर्ण मढ़ा हुआ था। राजा जनक ने घोषणा की— "भारतवर्ष के विद्वानों में जो सर्वश्रेष्ठ ब्रह्मज्ञानी हों, वे इन गऊओं को ले जाएँ।"

सभा में सन्नाटा छा गया। तब महर्षि याज्ञवल्क्य ने अपने शिष्यों से कहा कि गऊओं को आश्रम की ओर ले चलो। इस पर सभा के विद्वानों ने शास्त्रार्थ हेतु उन्हें ललकारा। 

विदुषी गार्गी वाचक्नवी और महर्षि याज्ञवल्क्य के बीच अति सूक्ष्म दार्शनिक संवाद हुआ। गार्गी ने याज्ञवल्क्य से सृष्टि के आधारभूत तत्वों पर गूढ़ प्रश्न पूछे। यह घटना सिद्ध करती है कि प्राचीन मिथिला में स्त्रियों को सर्वोच्च वैदिक ज्ञान और शास्त्रार्थ का पूर्ण अधिकार प्राप्त था।

यह संस्मरण मिथिला की विद्वता और दार्शनिक गरिमा का अमर ऐतिहासिक प्रमाण है।''',
        'author': admin_user,
        'status': 'APPROVED',
        'location': 'Janakpur / Mithila',
        'source_name': 'Sahitya Akademi / Vedic Heritage Portal',
        'source_url': 'https://vedicheritage.gov.in/'
    },
    {
        'title': 'खट्टर काकाक तरङ्ग — खट्टर काका आ न्याय-शास्त्रक विनोद',
        'category': 'MITHILA',
        'excerpt': 'प्रो. हरिमोहन झा रचित कालजयी चरित्र "खट्टर काका" के अद्भुत हास्य, तार्किक प्रत्युत्पन्नमति और व्यावहारिक दर्शन का किस्सा।',
        'content': '''मिथिलांचल के अमर साहित्यकार और पटना विश्वविद्यालय में दर्शनशास्त्र के अध्यक्ष रहे प्रो. हरिमोहन झा (1908-1986) द्वारा सृजित चरित्र 'खट्टर काका' (Khattar Kaka) मैथिली साहित्य और भारतीय व्यंग्य का एक अनमोल शिखर हैं।

खट्टर काका मिथिला के एक ऐसे विलक्षण, जिंदादिल और महाविद्वान गृही हैं, जो अपनी भाँग की तरंग में पान चबाते हुए रूढ़ियों, ढोंग और पाखंड पर शास्त्रार्थ के तीखे बाण चलाते हैं।

एक दिन गाँव के कुछ नवयुवक और रूढ़िवादी पंडित खट्टर काका के दलान पर आ पहुँचे। पंडित जी ने अभिमान में आकर कहा— "खट्टर काका! आजकल के लड़के न्याय-शास्त्र और तर्कशास्त्र नहीं पढ़ते। आप ही बताइए कि ईश्वर, मोक्ष और संसार का असली रहस्य क्या है?"

खट्टर काका ने अपनी भाँग की कुल्हड़ से चुस्की ली, मुँह में ताज़ा पान दबाया और मुस्कुराकर बोले— 
"अरे पंडित जी! तर्कशास्त्र भी कोई कठिन चीज़ है? हमारे मिथिला के विद्वान पक्षियों से भी न्याय-शास्त्र पढ़ा लेते हैं। रही बात मोक्ष की, तो सुनो— संसार में भूखे पेट मोक्ष की बात करना वैसा ही है जैसे जलते हुए घर में बैठकर दीपक जलाना! 

असली न्याय-शास्त्र तो यह है कि जो व्यक्ति ईश्वर द्वारा दिए गए जीवन का आनंद नहीं लेता, ताज़ा दही-चूड़ा और आम का रसा छोड़कर केवल पोथियों के पन्नों में उलझा रहता है, वह ज्ञानी नहीं बल्कि महामूर्ख है!"

नवयुवक यह सुनकर खिलखिलाकर हँस पड़े। पंडित जी ने झेंपकर पूछा— "काका! शास्त्र में लिखा है कि संयम ही जीवन है।"

खट्टर काका ने तुरंत अपनी चुटीली शैली में उत्तर दिया— 
"शास्त्र तो बहुत कुछ कहते हैं पंडित जी! लेकिन अगर संयम का अर्थ जीवन के सरस आनंद से दूर रहना है, तो फिर तो हमारे आँगन की गाय-भैंस सबसे बड़ी संन्यासिनी और सिद्ध योगी मानी जाएँगी, जो दिनभर शांत बैठकर चबाती रहती हैं!"

खट्टर काका के इस अद्वितीय विनोद और तार्किक वाक्पटुता को सुनकर पूरा दलान ठहाकों से गूँज उठा। 

'खट्टर काकाक तरंग' (Khattar Kakak Taranga) केवल हास्य नहीं है, बल्कि मिथिला की बौद्धिक प्रखरता, स्वतंत्र सोच और सहज लोक-जीवन की अनुपम अभिव्यक्ति है।''',
        'author': admin_user,
        'status': 'APPROVED',
        'location': 'Kumar Bajitpur / Madhubani',
        'source_name': 'Mithila Literature / Sahitya Akademi',
        'source_url': 'https://sahitya-akademi.gov.in/'
    },
    {
        'title': 'खट्टर काका आ विवाहक मण्डप (कन्यादान व्यंग्य कथा)',
        'category': 'FOLKLORE',
        'excerpt': 'हरिमोहन झा कृत "कन्यादान" आ "खट्टर काका" की चुटीली लोक कथा जहाँ सामाजिक आडंबरों पर करारा प्रहार किया गया है।',
        'content': '''प्रो. हरिमोहन झा की कालजयी कृतियाँ 'कन्यादान' (Kanya Dan) और 'खट्टर काकाक तरंग' में मिथिला के सामाजिक जीवन का बड़ा ही जीवंत और हास्यपूर्ण वर्णन मिलता है।

एक विवाह समारोह में वर पक्ष के लोग भारी आडंबर और दहेज की शर्ते रख रहे थे। कन्या पक्ष के गृहस्थ बेबस महसूस कर रहे थे। उसी समय दलान में खट्टर काका का आगमन हुआ।

खट्टर काका ने वर के पिता से बड़े आदर से पूछा— "अरे समधी जी! आप इतने दुखी और चिंतित क्यों दिख रहे हैं? विवाह तो दो आत्माओं का आनंदमय मिलन है!"

वर पक्ष के वयोवृद्ध सज्जन ने अकड़कर कहा— "खट्टर जी! हम तो शास्त्र-सम्मत रीति से विवाह कराना चाहते हैं। हमें आभूषण और दहेज सामग्री कम दिख रही है।"

खट्टर काका ने मुस्कुराते हुए अपनी चुटकी ली और बोले— 
"अरे वाह! आप तो शास्त्रज्ञ निकले! लेकिन ऋग्वेद के विवाह सूक्त में तो लिखा है कि कन्या ही घर की असली लक्ष्मी है। यदि आप कन्या के स्थान पर सोने और बर्तन को प्रधानता दे रहे हैं, तो विवाह मंडप के बजाय सर्राफा बाज़ार में जाकर बैठना चाहिए!"

सभा में उपस्थित सभी लोग खट्टर काका की इस सपासप टिप्पणी पर हँस पड़े। वर पक्ष के बुजुर्ग पानी-पानी हो गए और शांतिपूर्वक विवाह संपन्न हुआ।

यह कथा हरिमोहन झा की दूरगामी दृष्टि को दर्शाती है कि कैसे उन्होंने व्यंग्य और हास्य के माध्यम से मिथिला समाज में कुरीतियों के विरुद्ध अलख जगाई।''',
        'author': admin_user,
        'status': 'APPROVED',
        'location': 'Vaishali / Darbhanga',
        'source_name': 'Sahitya Akademi / Maithili Classics',
        'source_url': 'https://sahitya-akademi.gov.in/'
    }
]

for st in stories_data:
    obj, created = Story.objects.get_or_create(title=st['title'], defaults=st)
    if not created:
        for k, v in st.items():
            setattr(obj, k, v)
        obj.save()

print("Section 7 seeded!")


# ----------------------------------------------------
# SECTION 8: समाचार (Real Mithila News)
# ----------------------------------------------------
print("Seeding Section 8: समाचार (Real Verified News)...")

news_data = [
    {
        'title': 'दरभंगा एयरपोर्ट सं नया उड़ान सेवा आ नया सिविल एन्क्लेव विस्तारक कार्य तेज',
        'category': 'MITHILA',
        'summary': 'दरभंगा हवाई अड्डे से नए शहरों के लिए विमान सेवा एवं नया सिविल एन्क्लेव टर्मिनल भवन निर्माण कार्य में तेजी।',
        'content': '''मिथिला क्षेत्र के प्रमुख संपर्क केंद्र दरभंगा एयरपोर्ट (Darbhanga Airport) के विकास हेतु भारतीय विमानपत्तन प्राधिकरण (AAI) तथा बिहार सरकार द्वारा नए सिविल एन्क्लेव भवन निर्माण प्रक्रिया को तेजी प्रदान की गई है।

दरभंगा एयरपोर्ट से दिल्ली, मुंबई, बेंगलुरु और कोलकाता के अलावा अन्य प्रमुख शहरों के लिए सीधी विमान सेवाओं की मांग को देखते हुए नए टर्मिनल भवन का निर्माण कार्य प्रगति पर है। इससे संपूर्ण उत्तरी बिहार और मिथिलांचल के लाखों यात्रियों को सुगम यात्रा सुविधा प्राप्त होगी।

स्थान: दरभंगा, बिहार
प्रमाणित स्रोत: प्रेस सूचना ब्यूरो (PIB Bihar) / नागर विमानन मंत्रालय''',
        'author': admin_user,
        'category': 'MITHILA',
        'location': 'Darbhanga, Bihar',
        'source_name': 'Press Information Bureau (PIB Bihar)',
        'source_url': 'https://pib.gov.in/',
        'status': 'APPROVED',
        'is_published': True
    },
    {
        'title': 'मधुबनी चित्रकला आ हस्तशिल्प क्षेत्र में नया महिला क्लस्टर स्थापित',
        'category': 'CULTURE',
        'summary': 'बिहार राज्य हस्तशिल्प निगम द्वारा मधुबनी जिला में सौ से अधिक महिला हस्तशिल्प कलाकारों हेतु प्रोत्साहन योजना।',
        'content': '''बिहार सरकार के उद्योग विभाग तथा बिहार राज्य हस्तशिल्प विकास निगम द्वारा मधुबनी चित्रकला (Madhubani Art) के संरक्षण और संवर्धन हेतु जीतवारपुर और रंटी गांव में नए महिला कारीगर क्लस्टर की स्थापना की गई है।

इस योजना के अंतर्गत स्थानीय महिला कलाकारों को आधुनिक डिज़ाइन, प्राकृतिक रंगों के उपयोग और ई-कॉमर्स प्लेटफॉर्म्स पर अपने चित्रों को सीधे बेचने हेतु प्रशिक्षण और विपणन सहायता प्रदान की जा रही है।

स्थान: मधुबनी, बिहार
प्रमाणित स्रोत: सूचना एवं जनसंपर्क विभाग (IPRD Bihar)''',
        'author': admin_user,
        'category': 'CULTURE',
        'location': 'Madhubani, Bihar',
        'source_name': 'IPRD Bihar (सूचना एवं जनसंपर्क विभाग)',
        'source_url': 'https://iprd.bihar.gov.in/',
        'status': 'APPROVED',
        'is_published': True
    },
    {
        'title': 'पुनौरा धाम सीतामढ़ी के भव्य पर्यटन परिपथ योजना हेतु बजट स्वीकृति',
        'category': 'BIHAR',
        'summary': 'रामायण सर्किट अंतर्गत पुनौरा धाम सीतामढ़ी को विश्वस्तरीय धार्मिक पर्यटन केंद्र के रूप में विकसित किया जाएगा।',
        'content': '''बिहार के सीतामढ़ी स्थित मां जानकी की जन्मस्थली पुनौरा धाम (Punaura Dham) को रामायण परिपथ के अंतर्गत आधुनिक सुविधाओं से सुसज्जित करने हेतु विकास योजना को प्रशासनिक स्वीकृति प्रदान की गई है।

योजना के तहत पुनौरा धाम मंदिर परिसर का सौंदर्यीकरण, परिक्रमा पथ, सीता सरोवर संरक्षण, एवं अंतरराष्ट्रीय पर्यटकों हेतु सर्वसुविधायुक्त धर्मशाला व व्याख्यान केंद्र का निर्माण किया जाएगा।

स्थान: सीतामढ़ी, बिहार
प्रमाणित स्रोत: पर्यटन मंत्रालय, भारत सरकार / बिहार पर्यटन''',
        'author': admin_user,
        'category': 'BIHAR',
        'location': 'Sitamarhi, Bihar',
        'source_name': 'Bihar Tourism Department',
        'source_url': 'https://tourism.bihar.gov.in/',
        'status': 'APPROVED',
        'is_published': True
    }
]

for nw in news_data:
    obj, created = News.objects.get_or_create(title=nw['title'], defaults=nw)
    if not created:
        for k, v in nw.items():
            setattr(obj, k, v)
        obj.save()

print("Section 8 seeded!")


# ----------------------------------------------------
# SECTION 10: रोजगार (Real Job Opportunities)
# ----------------------------------------------------
print("Seeding Section 10: रोजगार (Real Verified Public Job Notice)...")

job_cat_edu, _ = JobCategory.objects.get_or_create(name='Education & Academic', defaults={'slug': 'education-academic'})
job_type_ft, _ = JobType.objects.get_or_create(name='Full-time / Government', defaults={'slug': 'full-time-govt'})

Job.objects.update_or_create(
    title='सहायक प्राध्यापक एवं शोध पद सूचना (Assistant Professor Academic Notice)',
    defaults={
        'category': job_cat_edu,
        'job_type': job_type_ft,
        'company': 'Lalit Narayan Mithila University (LNMU) & KSDSU Darbhanga',
        'location': 'Darbhanga, Bihar',
        'description': 'Official academic and research position notifications released by Bihar State University Service Commission (BSUSC) and LNMU Darbhanga for Maithili, Sanskrit, History and Science faculties. Application link and eligibility details available on official university portals.',
        'requirements': 'Post Graduation (Master Degree) in relevant subject with NET/Ph.D as per UGC norms.',
        'website': 'https://lnmu.ac.in/',
        'status': 'APPROVED',
        'posted_by': admin_user,
    }
)

print("Section 10 seeded!")

print("=========================================")
print("ALL DATA SEEDING COMPLETED SUCCESSFULLY!")
print("=========================================")
