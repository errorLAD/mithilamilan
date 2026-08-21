from django.core.management.base import BaseCommand
from core.models import State, City, Locality

class Command(BaseCommand):
    help = 'Seeds Indian states, major cities, and localities into the database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding pan-India location data...')

        locations_data = [
            {
                'state_name': 'Delhi NCR',
                'state_code': 'DL',
                'cities': [
                    {'name': 'Delhi NCR', 'popular': True, 'icon': '🏛️', 'localities': ['Connaught Place', 'South Extension', 'Hauz Khas', 'Saket', 'Lajpat Nagar', 'Dwarka', 'Rohini', 'Cyber City Gurgaon', 'Noida Sector 62']},
                ]
            },
            {
                'state_name': 'Maharashtra',
                'state_code': 'MH',
                'cities': [
                    {'name': 'Mumbai', 'popular': True, 'icon': '🌊', 'localities': ['Bandra West', 'Andheri East', 'Powai', 'Lower Parel', 'Juhu', 'Colaba']},
                    {'name': 'Pune', 'popular': True, 'icon': '🎓', 'localities': ['Koregaon Park', 'Viman Nagar', 'Baner', 'Hinjewadi', 'Kothrud']},
                ]
            },
            {
                'state_name': 'Karnataka',
                'state_code': 'KA',
                'cities': [
                    {'name': 'Bengaluru', 'popular': True, 'icon': '💻', 'localities': ['Indiranagar', 'Koramangala', 'HSR Layout', 'Whitefield', 'Electronic City', 'MG Road']},
                ]
            },
            {
                'state_name': 'Telangana',
                'state_code': 'TS',
                'cities': [
                    {'name': 'Hyderabad', 'popular': True, 'icon': 'Biryani', 'localities': ['HITEC City', 'Gachibowli', 'Jubilee Hills', 'Banjara Hills', 'Madhapur']},
                ]
            },
            {
                'state_name': 'Tamil Nadu',
                'state_code': 'TN',
                'cities': [
                    {'name': 'Chennai', 'popular': True, 'icon': '⛵', 'localities': ['T. Nagar', 'Adyar', 'Velachery', 'Anna Nagar', 'OMR']},
                ]
            },
            {
                'state_name': 'West Bengal',
                'state_code': 'WB',
                'cities': [
                    {'name': 'Kolkata', 'popular': True, 'icon': '🌉', 'localities': ['Park Street', 'Salt Lake', 'New Town', 'Ballygunge', 'Howrah']},
                ]
            },
            {
                'state_name': 'Rajasthan',
                'state_code': 'RJ',
                'cities': [
                    {'name': 'Jaipur', 'popular': True, 'icon': '🏰', 'localities': ['Pink City', 'Malviya Nagar', 'Vaishali Nagar', 'C-Scheme']},
                ]
            },
            {
                'state_name': 'Uttar Pradesh',
                'state_code': 'UP',
                'cities': [
                    {'name': 'Lucknow', 'popular': True, 'icon': '🕌', 'localities': ['Hazratganj', 'Gomti Nagar', 'Aliganj']},
                ]
            },
        ]

        for s_data in locations_data:
            state, _ = State.objects.get_or_create(
                name=s_data['state_name'],
                defaults={'code': s_data['state_code']}
            )
            for c_data in s_data['cities']:
                city, _ = City.objects.get_or_create(
                    state=state,
                    name=c_data['name'],
                    defaults={'is_popular': c_data['popular'], 'icon': c_data['icon']}
                )
                for loc_name in c_data['localities']:
                    Locality.objects.get_or_create(city=city, name=loc_name)

        self.stdout.write(self.style.SUCCESS('Successfully seeded pan-India locations!'))
