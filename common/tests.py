from django.test import TestCase
from django.urls import reverse
from athletes.models import Athlete
from competitions.models import Competition, CompetitionCategory
from records.models import Results
from datetime import date

class CommonViewsTest(TestCase):
    def setUp(self):
        comp_cat = CompetitionCategory.objects.create(category_name="OUTDOOR")
        self.athlete = Athlete.objects.create(
            first_name="A", last_name="B", nationality="BG",
            birth_date=date(1990, 1, 1), gender='M'
        )
        self.competition = Competition.objects.create(
            name="C", country="BG", city="S",
            start_date=date(2025, 1, 1), end_date=date(2025, 1, 2),
            category=comp_cat
        )

    def test_home_page_counts(self):
        response = self.client.get(reverse('common:home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['athletes_count'], 1)
        self.assertEqual(response.context['competitions_count'], 1)
        self.assertEqual(response.context['results_count'], 0)

    def test_disciplines_view(self):
        response = self.client.get(reverse('common:disciplines'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/disciplines.html')

    def test_contact_page_view(self):
        response = self.client.get(reverse('common:contact_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/contact.html')
