from django.test import TestCase
from django.urls import reverse
from cab_auto.models import DriverProfile

class CabAutoViewsTest(TestCase):
    def setUp(self):
        self.driver = DriverProfile.objects.create(
            full_name='Subhash Driver',
            slug='subhash-driver',
            mobile_number='9876543210',
            whatsapp_number='9876543210',
            vehicle_type='auto',
            vehicle_model='Bajaj Auto',
            service_area='Darbhanga',
            status='published'
        )

    def test_cab_auto_home_view(self):
        response = self.client.get(reverse('cab_auto:cab_auto_home'))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_view(self):
        response = self.client.get(reverse('cab_auto:driver_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subhash Driver')

    def test_driver_detail_view(self):
        response = self.client.get(reverse('cab_auto:driver_detail', kwargs={'slug': self.driver.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subhash Driver')
