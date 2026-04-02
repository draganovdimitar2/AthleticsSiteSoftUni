from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsViewsTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post(self):
        # Using a more complex password to avoid validators if possible, 
        # though by default test settings often don't enforce them unless specified.
        data = {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(reverse('accounts:register'), data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post(self):
        User.objects.create_user(username='testuser', password='StrongPass123!')
        data = {
            'username': 'testuser',
            'password': 'StrongPass123!',
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertRedirects(response, reverse('common:home_page'))

class AccessControlTest(TestCase):
    def test_anonymous_user_cannot_access_create_athlete(self):
        response = self.client.get(reverse('athletes:create'))
        # Should redirect to login
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('athletes:create')}")

    def test_anonymous_user_cannot_access_create_competition(self):
        response = self.client.get(reverse('competitions:create'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('competitions:create')}")

    def test_anonymous_user_can_access_list_athletes(self):
        response = self.client.get(reverse('athletes:list'))
        self.assertEqual(response.status_code, 200)
