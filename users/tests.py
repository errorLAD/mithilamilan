from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.password_reset_url = reverse('users:password_reset')

        self.user_data = {
            'username': 'mithilatech',
            'email': 'user@mithilamilan.in',
            'password1': 'Mithila@Pass123!',
            'password2': 'Mithila@Pass123!',
            'full_name': 'Janak Kumar Jha',
            'location': 'Darbhanga'
        }
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@mithilamilan.in',
            password='ExistingPass123!'
        )

    def test_signup_successful(self):
        response = self.client.post(self.signup_url, self.user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='mithilatech').exists())
        created_user = User.objects.get(username='mithilatech')
        self.assertEqual(created_user.email, 'user@mithilamilan.in')
        self.assertEqual(created_user.first_name, 'Janak')
        self.assertEqual(created_user.last_name, 'Kumar Jha')
        self.assertEqual(created_user.location, 'Darbhanga')
        # Check welcome message
        messages = list(response.context['messages'])
        self.assertTrue(any('mithila' in str(m).lower() or 'welcome' in str(m).lower() for m in messages))

    def test_signup_duplicate_username(self):
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'EXISTINGUSER'  # Case-insensitive duplicate check
        response = self.client.post(self.signup_url, duplicate_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.has_error('username'))

    def test_signup_duplicate_email(self):
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'EXISTING@mithilamilan.in'  # Case-insensitive check
        response = self.client.post(self.signup_url, duplicate_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.has_error('email'))

    def test_signup_password_mismatch(self):
        mismatch_data = self.user_data.copy()
        mismatch_data['password2'] = 'DifferentPassword123!'
        response = self.client.post(self.signup_url, mismatch_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.has_error('password2'))

    def test_login_by_username(self):
        response = self.client.post(self.login_url, {
            'username_or_email': 'existinguser',
            'password': 'ExistingPass123!',
            'remember_me': True
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_by_email(self):
        response = self.client.post(self.login_url, {
            'username_or_email': 'EXISTING@MITHILAMILAN.IN',
            'password': 'ExistingPass123!',
            'remember_me': True
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_invalid_password(self):
        response = self.client.post(self.login_url, {
            'username_or_email': 'existinguser',
            'password': 'WrongPassword123!'
        })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(any('invalid' in str(m).lower() for m in messages))

    def test_login_next_redirect(self):
        next_path = '/posts/create/'
        response = self.client.post(f"{self.login_url}?next={next_path}", {
            'username_or_email': 'existinguser',
            'password': 'ExistingPass123!'
        })
        self.assertRedirects(response, next_path)

    def test_logout(self):
        self.client.login(username='existinguser', password='ExistingPass123!')
        response = self.client.post(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_password_reset_flow(self):
        response = self.client.post(self.password_reset_url, {
            'email': 'existing@mithilamilan.in'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password Reset Request', mail.outbox[0].subject)
