#!/usr/bin/env python
"""
Data Loading Script for Athletics Site
Loads sample data into all 8 database tables:
1. athletes_athlete
2. athletes_agecategory
3. athletes_discipline
4. competitions_competitioncategory
5. competitions_competition
6. competitions_competition_age_groups
7. records_results
8. common (no models yet)
"""

import os
import django
from decimal import Decimal
from datetime import date, timedelta

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'athletics_site.settings')
django.setup()

from athletes.models import Athlete, AgeCategory, Discipline
from competitions.models import Competition, CompetitionCategory
from records.models import Results


def load_data():
    print("Starting data load...")

    # Clear existing data in the correct order (respecting foreign keys)
    print("Clearing existing data...")
    # Delete in reverse order of foreign key dependencies
    Results.objects.all().delete()
    print("  ✓ Cleared Results")

    Competition.objects.all().delete()
    print("  ✓ Cleared Competitions")

    # Now we can safely delete CompetitionCategory
    CompetitionCategory.objects.all().delete()
    print("  ✓ Cleared Competition Categories")

    # Clear athlete-related data
    Athlete.objects.all().delete()
    print("  ✓ Cleared Athletes")

    AgeCategory.objects.all().delete()
    print("  ✓ Cleared Age Categories")

    Discipline.objects.all().delete()
    print("  ✓ Cleared Disciplines")

    # 1. Create Disciplines
    print("\nCreating disciplines...")
    disciplines_data = [
        {'name': '100m Sprint'},
        {'name': '200m Sprint'},
        {'name': '400m Run'},
        {'name': '1500m Run'},
        {'name': '5000m Run'},
        {'name': 'Long Jump'},
        {'name': 'High Jump'},
        {'name': 'Shot Put'},
        {'name': 'Javelin Throw'},
        {'name': 'Pole Vault'},
    ]
    disciplines = {}
    for disc in disciplines_data:
        obj, created = Discipline.objects.get_or_create(**disc)
        disciplines[disc['name']] = obj
        if created:
            print(f"  ✓ Created: {disc['name']}")

    # 2. Create Age Categories
    print("\nCreating age categories...")
    # All age categories from your model, for both genders
    age_categories_data = [
        {'name': 'U14', 'gender': 'M'},
        {'name': 'U14', 'gender': 'F'},
        {'name': 'U16', 'gender': 'M'},
        {'name': 'U16', 'gender': 'F'},
        {'name': 'U18', 'gender': 'M'},
        {'name': 'U18', 'gender': 'F'},
        {'name': 'U20', 'gender': 'M'},
        {'name': 'U20', 'gender': 'F'},
        {'name': 'U23', 'gender': 'M'},
        {'name': 'U23', 'gender': 'F'},
        {'name': 'SEN', 'gender': 'M'},
        {'name': 'SEN', 'gender': 'F'},
        {'name': 'V35', 'gender': 'M'},
        {'name': 'V35', 'gender': 'F'},
        {'name': 'V40', 'gender': 'M'},
        {'name': 'V40', 'gender': 'F'},
        {'name': 'V45', 'gender': 'M'},
        {'name': 'V45', 'gender': 'F'},
        {'name': 'V50', 'gender': 'M'},
        {'name': 'V50', 'gender': 'F'},
        {'name': 'V55', 'gender': 'M'},
        {'name': 'V55', 'gender': 'F'},
        {'name': 'V60', 'gender': 'M'},
        {'name': 'V60', 'gender': 'F'},
    ]

    age_categories = {}
    for cat in age_categories_data:
        obj, created = AgeCategory.objects.get_or_create(**cat)
        age_categories[(cat['name'], cat['gender'])] = obj
        if created:
            print(f"  ✓ Created: {cat['name']} ({cat['gender']})")

    # 3. Create Athletes
    print("\nCreating athletes...")
    athletes_data = [
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'nationality': 'USA',
            'birth_date': date(2000, 5, 15),
            'gender': 'M',
            'disciplines': ['100m Sprint', '200m Sprint']
        },
        {
            'first_name': 'Emma',
            'last_name': 'Johnson',
            'nationality': 'UK',
            'birth_date': date(1999, 8, 22),
            'gender': 'F',
            'disciplines': ['400m Run', '1500m Run']
        },
        {
            'first_name': 'Michael',
            'last_name': 'Brown',
            'nationality': 'Canada',
            'birth_date': date(1994, 3, 10),
            'gender': 'M',
            'disciplines': ['Long Jump', 'High Jump']
        },
        {
            'first_name': 'Sarah',
            'last_name': 'Davis',
            'nationality': 'Australia',
            'birth_date': date(1984, 11, 30),
            'gender': 'F',
            'disciplines': ['5000m Run', 'Pole Vault']
        },
        {
            'first_name': 'David',
            'last_name': 'Wilson',
            'nationality': 'Germany',
            'birth_date': date(1990, 7, 18),
            'gender': 'M',
            'disciplines': ['Shot Put', 'Javelin Throw']
        },
        {
            'first_name': 'Anna',
            'last_name': 'Mueller',
            'nationality': 'Germany',
            'birth_date': date(1995, 2, 25),
            'gender': 'F',
            'disciplines': ['200m Sprint', '400m Run']
        },
    ]
    athletes = {}
    for athlete_data in athletes_data:
        disciplines_list = athlete_data.pop('disciplines')
        athlete, created = Athlete.objects.get_or_create(**athlete_data)
        athletes[f"{athlete_data['first_name']} {athlete_data['last_name']}"] = athlete

        # Add disciplines
        for disc_name in disciplines_list:
            athlete.disciplines.add(disciplines[disc_name])

        if created:
            print(f"  ✓ Created: {athlete_data['first_name']} {athlete_data['last_name']}")

    # 4. Create Competition Categories
    print("\nCreating competition categories...")
    comp_cat_data = [
        {'category_name': 'INDOOR'},
        {'category_name': 'OUTDOOR'},
    ]
    comp_categories = {}
    for cat in comp_cat_data:
        obj, created = CompetitionCategory.objects.get_or_create(**cat)
        comp_categories[cat['category_name']] = obj
        if created:
            print(f"  ✓ Created: {cat['category_name']}")

    # 5. Create Competitions
    print("\nCreating competitions...")
    today = date.today()
    competitions_data = [
        {
            'name': 'Spring Athletics Championship 2026',
            'country': 'USA',
            'city': 'New York',
            'start_date': today + timedelta(days=30),
            'end_date': today + timedelta(days=32),
            'category': comp_categories['OUTDOOR'],
            'age_groups_list': [('V35', 'M'), ('V35', 'F'), ('SEN', 'M'), ('SEN', 'F'), ('V40', 'M'), ('V40', 'F')],
        },
        {
            'name': 'European Indoor Championships',
            'country': 'Germany',
            'city': 'Berlin',
            'start_date': today + timedelta(days=60),
            'end_date': today + timedelta(days=63),
            'category': comp_categories['INDOOR'],
            'age_groups_list': [('V35', 'M'), ('V35', 'F'), ('SEN', 'M'), ('SEN', 'F'), ('V40', 'M'), ('V40', 'F')],
        },
        {
            'name': 'Summer Open Meet',
            'country': 'UK',
            'city': 'London',
            'start_date': today + timedelta(days=90),
            'end_date': today + timedelta(days=92),
            'category': comp_categories['OUTDOOR'],
            'age_groups_list': [('V35', 'M'), ('V35', 'F'), ('SEN', 'M'), ('SEN', 'F'), ('V40', 'M'), ('V40', 'F')],
        },
    ]
    competitions = {}
    for comp_data in competitions_data:
        age_groups = comp_data.pop('age_groups_list')
        competition, created = Competition.objects.get_or_create(
            name=comp_data['name'],
            country=comp_data['country'],
            defaults={
                'city': comp_data['city'],
                'start_date': comp_data['start_date'],
                'end_date': comp_data['end_date'],
                'category': comp_data['category'],
            }
        )
        competitions[comp_data['name']] = competition

        # Add age groups
        for age_cat in age_groups:
            competition.age_groups.add(age_categories[age_cat])

        if created:
            print(f"  ✓ Created: {comp_data['name']}")

    # 6. Create Results
    print("\nCreating results...")
    results_data = [
        {
            'athlete_name': 'John Smith',
            'competition_name': 'Spring Athletics Championship 2026',
            'discipline_name': '100m Sprint',
            'age_category': ('SEN', 'M'),
            'position': 1,
            'result_value': Decimal('10.50'),
        },
        {
            'athlete_name': 'John Smith',
            'competition_name': 'Spring Athletics Championship 2026',
            'discipline_name': '200m Sprint',
            'age_category': ('SEN', 'M'),
            'position': 2,
            'result_value': Decimal('21.35'),
        },
        {
            'athlete_name': 'Emma Johnson',
            'competition_name': 'Spring Athletics Championship 2026',
            'discipline_name': '400m Run',
            'age_category': ('SEN', 'F'),
            'position': 1,
            'result_value': Decimal('52.80'),
        },
        {
            'athlete_name': 'Michael Brown',
            'competition_name': 'European Indoor Championships',
            'discipline_name': 'Long Jump',
            'age_category': ('SEN', 'M'),
            'position': 3,
            'result_value': Decimal('7.45'),
        },
        {
            'athlete_name': 'Sarah Davis',
            'competition_name': 'Summer Open Meet',
            'discipline_name': '5000m Run',
            'age_category': ('V40', 'F'),
            'position': 1,
            'result_value': Decimal('1245.50'),
        },
        {
            'athlete_name': 'David Wilson',
            'competition_name': 'European Indoor Championships',
            'discipline_name': 'Shot Put',
            'age_category': ('V35', 'M'),
            'position': 2,
            'result_value': Decimal('18.75'),
        },
        {
            'athlete_name': 'Anna Mueller',
            'competition_name': 'Summer Open Meet',
            'discipline_name': '200m Sprint',
            'age_category': ('SEN', 'F'),
            'position': 2,
            'result_value': Decimal('23.45'),
        },
        {
            'athlete_name': 'Emma Johnson',
            'competition_name': 'European Indoor Championships',
            'discipline_name': '1500m Run',
            'age_category': ('SEN', 'F'),
            'position': 1,
            'result_value': Decimal('235.90'),
        },
    ]

    for result_data in results_data:
        athlete = athletes[result_data['athlete_name']]
        competition = competitions[result_data['competition_name']]
        discipline = disciplines[result_data['discipline_name']]
        age_category = age_categories[result_data['age_category']]

        result = Results.objects.create(
            athlete=athlete,
            competition=competition,
            discipline=discipline,
            age_category=age_category,
            position=result_data['position'],
            result_value=result_data['result_value'],
            result_date=competition.start_date,
        )
        print(f"  ✓ Created result: {result_data['athlete_name']} - {result_data['discipline_name']}")

    print("\n✅ Data loading completed successfully!")
    print(f"\nSummary:")
    print(f"  • Athletes: {Athlete.objects.count()}")
    print(f"  • Age Categories: {AgeCategory.objects.count()}")
    print(f"  • Disciplines: {Discipline.objects.count()}")
    print(f"  • Competition Categories: {CompetitionCategory.objects.count()}")
    print(f"  • Competitions: {Competition.objects.count()}")
    print(f"  • Results: {Results.objects.count()}")


if __name__ == '__main__':
    try:
        load_data()
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        import traceback

        traceback.print_exc()