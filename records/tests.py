from django.test import TestCase
from athletes.models import Athlete, AgeCategory, Discipline
from competitions.models import Competition, CompetitionCategory
from records.models import Results
from datetime import date


class RecordsModelTest(TestCase):
    def setUp(self):
        self.comp_cat = CompetitionCategory.objects.create(category_name="OUTDOOR")
        self.age_cat_u14 = AgeCategory.objects.create(name='U14', gender='M')
        self.age_cat_sen = AgeCategory.objects.create(name='SEN', gender='M')
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
        # Create result without explicitly setting age_category
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
