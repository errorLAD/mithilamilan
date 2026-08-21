import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redditClone.settings')
django.setup()

from store.models import Category, Artist, Product
from cab_auto.models import DriverProfile
from ghatkaiti.models import MatrimonialProfile
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

def seed_store():
    print("Seeding Mithila Store...")
    cat_paintings, _ = Category.objects.get_or_create(
        name='Madhubani Paintings',
        defaults={'icon': 'fa-palette', 'description': 'Handcrafted traditional Mithila folk art on handmade paper & canvas.'}
    )
    cat_clothing, _ = Category.objects.get_or_create(
        name='Traditional Clothing',
        defaults={'icon': 'fa-shirt', 'description': 'Tussar silk sarees, hand-painted dupattas, and kurtas.'}
    )
    cat_decor, _ = Category.objects.get_or_create(
        name='Home Décor',
        defaults={'icon': 'fa-house-chimney-window', 'description': 'Terracotta sculptures, bamboo crafts, and wall hangings.'}
    )
    cat_gifts, _ = Category.objects.get_or_create(
        name='Cultural Gifts',
        defaults={'icon': 'fa-gift', 'description': 'Mithila souvenir boxes, bookmarks, and hand-painted tea coasters.'}
    )

    artist1, _ = Artist.objects.get_or_create(
        name='Smt. Baua Devi',
        defaults={'location': 'Jitwarpur, Madhubani', 'specialty': 'Padma Shri Awardee - Master of Traditional Mithila Paintings', 'bio': 'Pioneer of Madhubani art on paper since 1966.'}
    )
    artist2, _ = Artist.objects.get_or_create(
        name='Kumari Sunita Jha',
        defaults={'location': 'Ranti Village, Madhubani', 'specialty': 'Fine Line Kachni Style & Modern Motifs', 'bio': 'Award-winning artisan specializing in intricate black ink Kachni artwork.'}
    )

    products_data = [
        {
            'title': 'Sita Ram Swayamvar Madhubani Painting',
            'category': cat_paintings,
            'artist': artist1,
            'price': 4500.00,
            'original_price': 6000.00,
            'stock_quantity': 5,
            'short_description': 'Authentic hand-painted depiction of Sita Ram Vivah using natural dyes on handmade paper.',
            'full_description': 'This exquisite piece depicts the divine union of Bhagwan Ram and Mata Sita at Mithila. Handcrafted using bamboo twigs and natural mineral pigments.',
            'material': 'Handmade Canvas Paper',
            'dimensions': '24 in x 18 in',
            'art_style': 'Traditional Bharni Style',
            'creation_details': 'Hand-drawn over 14 days using natural twig brushes and vegetable pigments.',
            'is_featured': True,
            'is_bestseller': True,
            'rating': 4.9,
        },
        {
            'title': 'Tree of Life (Kachni Style) Wall Art',
            'category': cat_paintings,
            'artist': artist2,
            'price': 3200.00,
            'original_price': 4000.00,
            'stock_quantity': 8,
            'short_description': 'Intricate fine-line peacock and Tree of Life motif in traditional black and red ink.',
            'full_description': 'Symbolizing prosperity and eternal fertility, the Tree of Life features flying peacocks and intricate floral borders.',
            'material': 'Handmade Paper with Silk Border',
            'dimensions': '20 in x 14 in',
            'art_style': 'Kachni Linework',
            'creation_details': 'Created with fine nib pens and permanent Indian ink.',
            'is_featured': True,
            'is_bestseller': False,
            'rating': 4.8,
        },
        {
            'title': 'Hand-painted Tussar Silk Saree',
            'category': cat_clothing,
            'artist': artist2,
            'price': 8900.00,
            'original_price': 11500.00,
            'stock_quantity': 3,
            'short_description': 'Pure Bhagalpuri Tussar silk saree featuring hand-painted Madhubani border and pallu.',
            'full_description': 'Royal Bhagalpuri Tussar silk adorned with hand-painted Ram-Sita motifs on the pallu and intricate floral borders.',
            'material': '100% Pure Tussar Silk',
            'dimensions': '6.5 meters with blouse piece',
            'art_style': 'Mithila Silk Painting',
            'creation_details': 'Takes over 25 days of delicate hand painting.',
            'is_featured': True,
            'is_bestseller': True,
            'rating': 5.0,
        },
        {
            'title': 'Terracotta Mithila Elephant Sculpture',
            'category': cat_decor,
            'artist': None,
            'price': 1490.00,
            'original_price': 1990.00,
            'stock_quantity': 12,
            'short_description': 'Handcrafted clay elephant decorated with traditional Mithila geometric patterns.',
            'full_description': 'Traditional welcoming decor piece for home entrance, baked in village kilns and hand-painted.',
            'material': 'Natural Terracotta Clay',
            'dimensions': '10 in x 8 in',
            'art_style': 'Terracotta Craft',
            'creation_details': 'Hand-molded and baked at high temperatures.',
            'is_featured': False,
            'is_bestseller': True,
            'rating': 4.7,
        },
    ]

    for pdata in products_data:
        Product.objects.get_or_create(title=pdata['title'], defaults=pdata)

    print("Store seeded!")

def seed_cab_auto():
    print("Seeding Cab & Auto...")
    drivers = [
        {
            'full_name': 'Ramesh Kumar Paswan',
            'age': 34,
            'mobile_number': '9876543210',
            'whatsapp_number': '9876543210',
            'vehicle_type': 'auto',
            'vehicle_model': 'Bajaj RE Maxima Green E-Auto',
            'vehicle_number': 'BR-07-PA-4521',
            'service_area': 'Darbhanga Station, Tower Chowk, Laheriasarai',
            'experience_years': 8,
            'available_hours': '5:00 AM - 11:00 PM',
            'about': 'Reliable auto driver available for local Darbhanga city trips and train station drops.',
            'status': 'published',
            'is_verified': True,
            'is_featured': True,
        },
        {
            'full_name': 'Subhash Chandra Jha',
            'age': 42,
            'mobile_number': '9123456789',
            'whatsapp_number': '9123456789',
            'vehicle_type': 'taxi',
            'vehicle_model': 'Maruti Swift Dzire VXI AC Cab',
            'vehicle_number': 'BR-32-P-8899',
            'service_area': 'Darbhanga Airport, Patna Outstation, Madhubani',
            'experience_years': 12,
            'available_hours': '24/7 Available',
            'about': 'Commercial driver badge holder with clean AC cab for Patna Airport drops and outstation family trips.',
            'status': 'published',
            'is_verified': True,
            'is_featured': True,
        }
    ]

    for d in drivers:
        DriverProfile.objects.get_or_create(full_name=d['full_name'], defaults=d)

    print("Cab & Auto seeded!")

def seed_ghatkaiti():
    print("Seeding Ghatkaiti Matrimonial...")
    profiles = [
        {
            'looking_for': 'son',
            'gender': 'male',
            'full_name': 'Aditya Jha',
            'age': 28,
            'height': "5' 10\"",
            'education': 'B.Tech (IIT Delhi), M.S. Computer Science',
            'profession': 'Senior Software Engineer at MNC (Noida)',
            'location': 'Noida / Delhi NCR',
            'native_place': 'Pandaul, Madhubani',
            'current_city': 'Noida, UP',
            'community_family_details': 'Kashyap Gotra, reputed Maithil Brahmin family.',
            'about_person': 'Simple, cultured Maithil youth with strong family values, fond of classical music and traveling.',
            'family_info': 'Father is a retired Bank Manager, mother is a homemaker. One younger sister pursuing MBBS.',
            'expectations': 'Looking for an educated, family-oriented bride from a respectable Mithila background.',
            'contact_person_name': 'Shri R.K. Jha (Father)',
            'whatsapp_number': '9876500112',
            'status': 'published',
            'is_verified': True,
            'is_featured': True,
        },
        {
            'looking_for': 'daughter',
            'gender': 'female',
            'full_name': 'Priyanka Chaudhary',
            'age': 26,
            'height': "5' 5\"",
            'education': 'M.Sc Biotechnology (DU), B.Ed',
            'profession': 'Assistant Professor at University',
            'location': 'South Delhi',
            'native_place': 'Darbhanga Town',
            'current_city': 'New Delhi',
            'community_family_details': 'Vatsa Gotra, ancestral roots in Darbhanga.',
            'about_person': 'Graceful, intelligent, and artistic girl adept in Mithila art and academic teaching.',
            'family_info': 'Father is a Govt Officer in Delhi, mother is a School Principal.',
            'expectations': 'Looking for a well-settled professional groom with good values and family mindset.',
            'contact_person_name': 'Smt. Sunita Chaudhary (Mother)',
            'whatsapp_number': '9876500334',
            'status': 'published',
            'is_verified': True,
            'is_featured': True,
        }
    ]

    for p in profiles:
        MatrimonialProfile.objects.get_or_create(full_name=p['full_name'], defaults=p)

    print("Ghatkaiti seeded!")

if __name__ == '__main__':
    seed_store()
    seed_cab_auto()
    seed_ghatkaiti()
    print("All seeding completed successfully!")
