from django.test import TestCase, Client
from django.urls import reverse
from core.models import State, City, Locality

class LocationAndCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.state = State.objects.create(name='Delhi NCR', code='DL')
        self.city = City.objects.create(state=self.state, name='Delhi NCR', is_popular=True)
        self.locality = Locality.objects.create(city=self.city, name='Connaught Place')

    def test_home_page_returns_200(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_set_location_view(self):
        response = self.client.post(reverse('core:set_location'), {'city_slug': self.city.slug})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('active_city_slug'), self.city.slug)
