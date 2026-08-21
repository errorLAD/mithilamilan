from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product, Cart, Order

class StoreModelViewsTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            title='Test Painting',
            slug='test-painting',
            category=self.cat,
            price=1000.00,
            original_price=1200.00,
            stock_quantity=10,
            short_description='Short desc',
            full_description='Full desc',
            is_active=True
        )

    def test_store_home_view(self):
        response = self.client.get(reverse('store:store_home'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Painting')

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Painting')

    def test_add_to_cart(self):
        response = self.client.post(reverse('store:add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 2})
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        self.assertEqual(cart.total_items, 2)
