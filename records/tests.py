from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from athletes.models import Athlete, AgeCategory, Discipline
from competitions.models import Competition, CompetitionCategory
from records.models import Results
from datetime import date


class RecordsModelTest(TestCase):
    def setUp(self):
        self.comp_cat = CompetitionCategory.objects.create(category_name="OUTDOOR")
        self.age_cat_u14 = AgeCategory.objects.create(name='U14', gender='M', min_age=None, max_age=13)
        self.age_cat_sen = AgeCategory.objects.create(name='SEN', gender='M', min_age=20, max_age=None)
        self.discipline = Discipline.objects.create(name="100m")

        self.competition = Competition.objects.create(
            name="Test Competition",
            country="Bulgaria",
            city="Sofia",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 10),
            category=self.comp_cat
        )
        self.competition.age_groups.add(self.age_cat_u14, self.age_cat_sen)

        # Athlete born 2012, in 2025 they are 13 -> U14
        self.athlete_u14 = Athlete.objects.create(
            first_name="Young",
            last_name="Boy",
            nationality="BG",
            birth_date=date(2012, 1, 1),
            gender='M'
        )

    def test_auto_assign_age_category(self):
        # create a result without explicitly setting age_category
        result = Results(
            athlete=self.athlete_u14,
            competition=self.competition,
            discipline=self.discipline,
            position=1,
            result_value=12.50,
            result_date=date(2025, 1, 5)
        )
        result.save()
        self.assertEqual(result.age_category, self.age_cat_u14)

    def test_invalid_result_date(self):
        # Result date outside competition dates
        result = Results(
            athlete=self.athlete_u14,
            competition=self.competition,
            discipline=self.discipline,
            position=1,
            result_value=12.50,
            result_date=date(2025, 1, 11) # After end_date
        )
        with self.assertRaises(ValidationError):
            result.save()

    def test_gender_mismatch_validation(self):
        female_athlete = Athlete.objects.create(
            first_name="Jane", last_name="Doe", nationality="BG",
            birth_date=date(2012, 1, 1), gender='F'
        )
        # trying to assign male age category to female athlete
        result = Results(
            athlete=female_athlete,
            competition=self.competition,
            discipline=self.discipline,
            age_category=self.age_cat_u14, # Male category
            position=1,
            result_value=12.50,
            result_date=date(2025, 1, 5)
        )
        with self.assertRaises(ValidationError):
            result.save()

class RecordsViewsTest(TestCase):
    def test_results_list_view(self):
        response = self.client.get(reverse('results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/list.html')
