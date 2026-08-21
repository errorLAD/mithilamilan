from django.test import TestCase
from django.urls import reverse
from ghatkaiti.models import MatrimonialProfile

class GhatkaitiViewsTest(TestCase):
    def setUp(self):
        self.profile = MatrimonialProfile.objects.create(
            looking_for='son',
            gender='male',
            full_name='Rohan Jha',
            slug='rohan-jha',
            age=27,
            education='B.Tech',
            profession='Engineer',
            location='Delhi',
            native_place='Madhubani',
            contact_person_name='S. Jha',
            whatsapp_number='9876543210',
            about_person='About text',
            family_info='Family text',
            expectations='Expectations text',
            status='published'
        )

    def test_profile_list_view(self):
        response = self.client.get(reverse('ghatkaiti:profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rohan Jha')

    def test_profile_detail_view(self):
        response = self.client.get(reverse('ghatkaiti:profile_detail', kwargs={'slug': self.profile.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rohan Jha')
