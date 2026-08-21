from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from events.models import Event, EventScheduleDay
from pandits.models import PanditProfile, ConsultationRequest
from mithila_pride.models import MithilaPride

class EventsAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            title='Durga Puja 2026',
            category='festival',
            short_description='Grand 5-day festival',
            about='Detailed Durga Puja info',
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 15),
            location='Darbhanga, Bihar',
            status='published',
            is_featured=True
        )
        self.schedule_day = EventScheduleDay.objects.create(
            event=self.event,
            day_number=1,
            date=date(2026, 10, 10),
            title='Day 1 Maha Saptami',
            morning_program='Navapatrika Snan'
        )

    def test_event_list_view(self):
        response = self.client.get(reverse('events:event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Durga Puja 2026')

    def test_event_detail_view(self):
        response = self.client.get(reverse('events:event_detail', kwargs={'slug': self.event.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Day 1 Maha Saptami')

    def test_event_ics_export(self):
        response = self.client.get(reverse('events:event_ics', kwargs={'slug': self.event.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/calendar')

class PanditsAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = PanditProfile.objects.create(
            full_name='Pandit Rameshwar Jha',
            profile_type='pandit',
            designation='Vedic Scholar',
            whatsapp_number='919876543210',
            location='Darbhanga, Bihar',
            experience_years=15,
            languages='Maithili, Hindi',
            specialization='Griha Pravesh',
            services_offered='Pujas and Rituals',
            about='Vedic Priest background',
            status='published',
            is_verified=True
        )

    def test_pandit_list_view(self):
        response = self.client.get(reverse('pandits:profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pandit Rameshwar Jha')

    def test_whatsapp_url_cleaner(self):
        self.assertEqual(self.profile.clean_whatsapp_number, '919876543210')
        self.assertIn('https://wa.me/919876543210', self.profile.get_whatsapp_url())

    def test_consultation_request_submission(self):
        response = self.client.post(reverse('pandits:pandit_detail', kwargs={'slug': self.profile.slug}), {
            'user_name': 'Devotee User',
            'user_phone': '9876543210',
            'user_whatsapp': '9876543210',
            'service_required': 'Griha Pravesh Puja',
            'preferred_date': '2026-11-15',
            'preferred_time': '10:00 AM',
            'location_type': 'offline',
            'message': 'Please confirm availability'
        })
        # Should redirect to WhatsApp URL
        self.assertEqual(response.status_code, 302)
        self.assertIn('https://wa.me/', response.url)
        self.assertEqual(ConsultationRequest.objects.count(), 1)

class MithilaPrideAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = MithilaPride.objects.create(
            full_name='Dr. Kameshwar Singh',
            category='scholar',
            era_generation='20th_century',
            place_location='Darbhanga, Bihar',
            biography='Visionary scholar and philanthropist',
            contributions_to_mithila='Founded Sanskrit University',
            status='published',
            is_featured=True
        )

    def test_person_list_view(self):
        response = self.client.get(reverse('mithila_pride:person_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Kameshwar Singh')

    def test_person_detail_view(self):
        response = self.client.get(reverse('mithila_pride:person_detail', kwargs={'slug': self.person.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Founded Sanskrit University')
