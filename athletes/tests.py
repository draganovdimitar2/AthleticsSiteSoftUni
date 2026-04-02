from django.test import TestCase
from django.urls import reverse
from athletes.models import Athlete, Discipline, AgeCategory
from datetime import date
from athletes.utils import calculate_age
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AthletesUtilsTest(TestCase):
    def test_calculate_age_before_birthday(self):
        birth_date = date(2000, 5, 20)
        on_date = date(2024, 5, 19)
        self.assertEqual(calculate_age(birth_date, on_date), 23)

    def test_calculate_age_after_birthday(self):
        birth_date = date(2000, 5, 20)
        on_date = date(2024, 5, 21)
        self.assertEqual(calculate_age(birth_date, on_date), 24)

    def test_calculate_age_on_birthday(self):
        birth_date = date(2000, 5, 20)
        on_date = date(2024, 5, 20)
        self.assertEqual(calculate_age(birth_date, on_date), 24)

class AthletesViewsTest(TestCase):
    def setUp(self):
        self.discipline = Discipline.objects.create(name="100m")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.athlete = Athlete.objects.create(
            first_name="John",
            last_name="Doe",
            nationality="USA",
            birth_date=date(1990, 1, 1),
            gender='M'
        )
        self.athlete.disciplines.add(self.discipline)

    def test_overview_view(self):
        response = self.client.get(reverse('athletes:overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'athletes/overview.html')

    def test_list_athletes_view(self):
        # Publicly accessible
        response = self.client.get(reverse('athletes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")
        self.assertEqual(len(response.context['athletes']), 1)

    def test_create_athlete_view_get(self):
        # Protected view, needs login
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('athletes:create'))
        self.assertEqual(response.status_code, 200)

    def test_create_athlete_view_post(self):
        # Protected view, needs login
        self.client.login(username='testuser', password='password123')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'nationality': 'UK',
            'birth_date': '1995-05-05',
            'gender': 'F',
            'disciplines': [self.discipline.id]
        }
        response = self.client.post(reverse('athletes:create'), data)
        self.assertRedirects(response, reverse('athletes:list'))
        self.assertTrue(Athlete.objects.filter(first_name='Jane').exists())

class AthleteAPITest(APITestCase):
    def setUp(self):
        self.discipline = Discipline.objects.create(name="200m")
        self.athlete = Athlete.objects.create(
            first_name="API", last_name="User", nationality="US",
            birth_date=date(1995, 1, 1), gender='M'
        )
        self.user = User.objects.create_user(username='apiuser', password='password123')
        self.list_url = reverse('athletes:athlete-api-list')

    def test_get_athletes_list_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_athlete_api_unauthorized(self):
        data = {'first_name': 'Unauthorized'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_athlete_api_authorized(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'first_name': 'New',
            'last_name': 'Athlete',
            'nationality': 'BG',
            'birth_date': '2000-01-01',
            'gender': 'M',
            'discipline_ids': [self.discipline.id]
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
