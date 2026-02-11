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

import random

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

    # Set a fixed 'today' date for consistent age calculation across data loading
    # This prevents age-related logic from shifting based on the actual current date
    today = date(2026, 2, 11) # Example fixed date: February 11, 2026


    # Helper function to calculate age at a specific date
    def calculate_age(birth_date, current_date):
        if not birth_date:
            return 0  # Or handle as error
        age = current_date.year - birth_date.year - (
                    (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        return age


    # Helper function to get age category for an athlete based on their age and gender
    def get_age_category_key(age, gender, age_categories_map):
        # This function assumes age_categories_map contains all AgeCategory objects
        # indexed by their (name, gender) tuple key, and each object has min_age/max_age.

        # Prioritize veteran categories if applicable
        if age >= 35:
            # Check veteran categories in descending order to catch the correct one
            for category_name_prefix in ['V60', 'V55', 'V50', 'V45', 'V40', 'V35']:
                key = (category_name_prefix, gender)
                cat_obj = age_categories_map.get(key)
                if cat_obj and cat_obj.min_age <= age and (cat_obj.max_age is None or age <= cat_obj.max_age):
                    return key

        # Check general age categories
        # Sort categories to ensure U14 is checked before U16 etc.
        general_categories_order = [
            'U14', 'U16', 'U18', 'U20', 'U23', 'SEN'
        ]

        for category_name_prefix in general_categories_order:
            key = (category_name_prefix, gender)
            cat_obj = age_categories_map.get(key)
            if cat_obj and cat_obj.min_age <= age and (cat_obj.max_age is None or age <= cat_obj.max_age):
                return key

        return None  # No matching category found

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
        {'name': '800m Run'},
        {'name': '1500m Run'},
        {'name': '3000m Run'},
        {'name': '5000m Run'},
        {'name': '10000m Run'},
        {'name': 'Long Jump'},
        {'name': 'High Jump'},
        {'name': 'Triple Jump'},
        {'name': 'Pole Vault'},
        {'name': 'Shot Put'},
        {'name': 'Discus Throw'},
        {'name': 'Javelin Throw'},
        {'name': 'Hammer Throw'},
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
    # These will automatically set min_age and max_age on save
    age_categories_data_raw = [
        {'name': 'U14', 'gender': 'M'}, {'name': 'U14', 'gender': 'F'},
        {'name': 'U16', 'gender': 'M'}, {'name': 'U16', 'gender': 'F'},
        {'name': 'U18', 'gender': 'M'}, {'name': 'U18', 'gender': 'F'},
        {'name': 'U20', 'gender': 'M'}, {'name': 'U20', 'gender': 'F'},
        {'name': 'U23', 'gender': 'M'}, {'name': 'U23', 'gender': 'F'},
        {'name': 'SEN', 'gender': 'M'}, {'name': 'SEN', 'gender': 'F'},
        {'name': 'V35', 'gender': 'M'}, {'name': 'V35', 'gender': 'F'},
        {'name': 'V40', 'gender': 'M'}, {'name': 'V40', 'gender': 'F'},
        {'name': 'V45', 'gender': 'M'}, {'name': 'V45', 'gender': 'F'},
        {'name': 'V50', 'gender': 'M'}, {'name': 'V50', 'gender': 'F'},
        {'name': 'V55', 'gender': 'M'}, {'name': 'V55', 'gender': 'F'},
        {'name': 'V60', 'gender': 'M'}, {'name': 'V60', 'gender': 'F'},
    ]

    age_categories = {} # This will store AgeCategory objects indexed by (name, gender) key
    for cat_raw in age_categories_data_raw:
        obj, created = AgeCategory.objects.get_or_create(**cat_raw)
        # Force save to ensure min_age/max_age are set immediately
        if created: # Only save if newly created to trigger the custom save method
            obj.save()
        age_categories[(cat_raw['name'], cat_raw['gender'])] = obj
        if created:
            print(f"  ✓ Created: {cat_raw['name']} ({cat_raw['gender']})")

    # 3. Create Athletes
    print("\nCreating athletes...")
    athletes_data = [
        # U14
        {
            'first_name': 'Leo', 'last_name': 'Garcia', 'nationality': 'ESP',
            'birth_date': today - timedelta(days=13 * 365 + 100), 'gender': 'M',
            'disciplines': ['100m Sprint', 'Long Jump']
        },
        {
            'first_name': 'Mia', 'last_name': 'Rodriguez', 'nationality': 'ESP',
            'birth_date': today - timedelta(days=12 * 365 + 200), 'gender': 'F',
            'disciplines': ['200m Sprint', 'High Jump']
        },
        # U16
        {
            'first_name': 'Noah', 'last_name': 'Miller', 'nationality': 'USA',
            'birth_date': today - timedelta(days=15 * 365 + 50), 'gender': 'M',
            'disciplines': ['400m Run', '800m Run']
        },
        {
            'first_name': 'Ava', 'last_name': 'Taylor', 'nationality': 'USA',
            'birth_date': today - timedelta(days=14 * 365 + 300), 'gender': 'F',
            'disciplines': ['1500m Run', '3000m Run']
        },
        # U18
        {
            'first_name': 'Liam', 'last_name': 'Wilson', 'nationality': 'GBR',
            'birth_date': today - timedelta(days=17 * 365 + 80), 'gender': 'M',
            'disciplines': ['Pole Vault', 'Triple Jump']
        },
        {
            'first_name': 'Isabella', 'last_name': 'Moore', 'nationality': 'GBR',
            'birth_date': today - timedelta(days=16 * 365 + 150), 'gender': 'F',
            'disciplines': ['Shot Put', 'Discus Throw']
        },
        # U20
        {
            'first_name': 'Lucas', 'last_name': 'Davies', 'nationality': 'AUS',
            'birth_date': today - timedelta(days=19 * 365 + 20), 'gender': 'M',
            'disciplines': ['Javelin Throw', 'Hammer Throw']
        },
        {
            'first_name': 'Sophia', 'last_name': 'White', 'nationality': 'AUS',
            'birth_date': today - timedelta(days=18 * 365 + 250), 'gender': 'F',
            'disciplines': ['100m Sprint', '200m Sprint']
        },
        # U23
        {
            'first_name': 'Ethan', 'last_name': 'Harris', 'nationality': 'CAN',
            'birth_date': today - timedelta(days=22 * 365 + 10), 'gender': 'M',
            'disciplines': ['400m Run', 'Long Jump']
        },
        {
            'first_name': 'Olivia', 'last_name': 'Martin', 'nationality': 'CAN',
            'birth_date': today - timedelta(days=21 * 365 + 120), 'gender': 'F',
            'disciplines': ['1500m Run', 'High Jump']
        },
        # SENIOR
        {
            'first_name': 'Daniel', 'last_name': 'Jackson', 'nationality': 'USA',
            'birth_date': today - timedelta(days=25 * 365), 'gender': 'M',
            'disciplines': ['100m Sprint', '200m Sprint', 'Long Jump']
        },
        {
            'first_name': 'Grace', 'last_name': 'Lee', 'nationality': 'KOR',
            'birth_date': today - timedelta(days=28 * 365 + 60), 'gender': 'F',
            'disciplines': ['400m Run', '800m Run']
        },
        # VETERANS
        {
            'first_name': 'Oliver', 'last_name': 'Scott', 'nationality': 'NZL',
            'birth_date': today - timedelta(days=36 * 365 + 30), 'gender': 'M', # V35
            'disciplines': ['5000m Run', '10000m Run']
        },
        {
            'first_name': 'Chloe', 'last_name': 'Green', 'nationality': 'NZL',
            'birth_date': today - timedelta(days=42 * 365 + 90), 'gender': 'F', # V40
            'disciplines': ['Shot Put', 'Discus Throw']
        },
        {
            'first_name': 'Max', 'last_name': 'Adams', 'nationality': 'GER',
            'birth_date': today - timedelta(days=48 * 365 + 110), 'gender': 'M', # V45
            'disciplines': ['Javelin Throw', 'Hammer Throw']
        },
        {
            'first_name': 'Lily', 'last_name': 'Baker', 'nationality': 'GER',
            'birth_date': today - timedelta(days=53 * 365 + 180), 'gender': 'F', # V50
            'disciplines': ['100m Sprint', 'Long Jump']
        },
        {
            'first_name': 'Jack', 'last_name': 'Turner', 'nationality': 'FRA',
            'birth_date': today - timedelta(days=58 * 365 + 210), 'gender': 'M', # V55
            'disciplines': ['High Jump', 'Pole Vault']
        },
        {
            'first_name': 'Zoe', 'last_name': 'Harris', 'nationality': 'FRA',
            'birth_date': today - timedelta(days=62 * 365 + 300), 'gender': 'F', # V60
            'disciplines': ['200m Sprint', 'Triple Jump']
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
        {'category_name': 'CHAMPIONSHIP'}, # Added new category
        {'category_name': 'MASTERS'}, # Added new category for veterans
    ]
    comp_categories = {}
    for cat in comp_cat_data:
        obj, created = CompetitionCategory.objects.get_or_create(**cat)
        comp_categories[cat['category_name']] = obj
        if created:
            print(f"  ✓ Created: {cat['category_name']}")

    # 5. Create Competitions
    print("\nCreating competitions...")
    competitions_data = [
        {
            'name': 'National Youth Games',
            'country': 'USA',
            'city': 'Los Angeles',
            'start_date': today + timedelta(days=45),
            'end_date': today + timedelta(days=47),
            'category': comp_categories['OUTDOOR'],
            'age_groups_list': [
                ('U14', 'M'), ('U14', 'F'), ('U16', 'M'), ('U16', 'F'),
                ('U18', 'M'), ('U18', 'F'), ('U20', 'M'), ('U20', 'F'),
            ],
        },
        {
            'name': 'International Grand Prix',
            'country': 'France',
            'city': 'Paris',
            'start_date': today + timedelta(days=90),
            'end_date': today + timedelta(days=91),
            'category': comp_categories['CHAMPIONSHIP'],
            'age_groups_list': [('SEN', 'M'), ('SEN', 'F'), ('U23', 'M'), ('U23', 'F')],
        },
        {
            'name': 'Masters Athletics Championship',
            'country': 'Germany',
            'city': 'Munich',
            'start_date': today + timedelta(days=120),
            'end_date': today + timedelta(days=122),
            'category': comp_categories['MASTERS'],
            'age_groups_list': [
                ('V35', 'M'), ('V35', 'F'), ('V40', 'M'), ('V40', 'F'),
                ('V45', 'M'), ('V45', 'F'), ('V50', 'M'), ('V50', 'F'),
                ('V55', 'M'), ('V55', 'F'), ('V60', 'M'), ('V60', 'F'),
            ],
        },
        {
            'name': 'Spring Athletics Championship 2026',
            'country': 'USA',
            'city': 'New York',
            'start_date': today + timedelta(days=30),
            'end_date': today + timedelta(days=32),
            'category': comp_categories['OUTDOOR'],
            'age_groups_list': [('SEN', 'M'), ('SEN', 'F'), ('U23', 'M'), ('U23', 'F')], # Adjusted for SEN/U23
        },
        {
            'name': 'European Indoor Championships',
            'country': 'Germany',
            'city': 'Berlin',
            'start_date': today + timedelta(days=60),
            'end_date': today + timedelta(days=63),
            'category': comp_categories['INDOOR'],
            'age_groups_list': [('SEN', 'M'), ('SEN', 'F'), ('U23', 'M'), ('U23', 'F')], # Adjusted for SEN/U23
        },
        {
            'name': 'Summer Open Meet',
            'country': 'UK',
            'city': 'London',
            'start_date': today + timedelta(days=90),
            'end_date': today + timedelta(days=92),
            'category': comp_categories['OUTDOOR'],
            'age_groups_list': [('SEN', 'M'), ('SEN', 'F'), ('U23', 'M'), ('U23', 'F')], # Adjusted for SEN/U23
        },
    ]
    competitions = {}
    for comp_data in competitions_data:
        age_groups_keys = comp_data.pop('age_groups_list')
        competition, created = Competition.objects.get_or_create(
            name=comp_data['name'],
            country=comp_data['country'],
            city=comp_data['city'],
            defaults={
                'start_date': comp_data['start_date'],
                'end_date': comp_data['end_date'],
                'category': comp_data['category'],
            }
        )
        competitions[comp_data['name']] = competition

        # Add age groups
        for age_cat_key in age_groups_keys:
            competition.age_groups.add(age_categories[age_cat_key])

        if created:
            print(f"  ✓ Created: {comp_data['name']}")

    # 6. Create Results
    print("\nCreating results...")
    results_data = []

    # Helper to create a result entry
    def add_result(athlete_name, competition_name, discipline_name, position, result_value):
        athlete_obj = athletes[athlete_name]
        competition_obj = competitions[competition_name]
        discipline_obj = disciplines[discipline_name]

        # Calculate age at competition start date
        athlete_age_at_comp = calculate_age(athlete_obj.birth_date, competition_obj.start_date)
        
        # Determine age category key based on calculated age and athlete's gender
        age_category_key = get_age_category_key(athlete_age_at_comp, athlete_obj.gender, age_categories)
        
        if age_category_key:
            results_data.append({
                'athlete_name': athlete_name,
                'competition_name': competition_name,
                'discipline_name': discipline_name,
                'age_category': age_category_key, # Use the determined key
                'position': position,
                'result_value': Decimal(str(result_value)),
            })
        else:
            print(f"  ❌ Warning: Could not determine age category for {athlete_name} (age {athlete_age_at_comp}, gender {athlete_obj.gender}) at {competition_name}. Skipping result.")


    # Add results for various athletes and competitions
    # National Youth Games
    add_result('Leo Garcia', 'National Youth Games', '100m Sprint', 1, 12.5) # U14 M
    add_result('Mia Rodriguez', 'National Youth Games', '200m Sprint', 2, 28.1) # U14 F
    add_result('Noah Miller', 'National Youth Games', '400m Run', 1, 55.0) # U16 M
    add_result('Ava Taylor', 'National Youth Games', '1500m Run', 1, 305.2) # U16 F
    add_result('Liam Wilson', 'National Youth Games', 'Pole Vault', 1, 3.80) # U18 M
    add_result('Isabella Moore', 'National Youth Games', 'Shot Put', 1, 11.50) # U18 F
    add_result('Lucas Davies', 'National Youth Games', 'Javelin Throw', 1, 45.0) # U20 M
    add_result('Sophia White', 'National Youth Games', '100m Sprint', 2, 13.1) # U20 F

    # International Grand Prix
    add_result('Ethan Harris', 'International Grand Prix', '400m Run', 3, 49.5) # U23 M
    add_result('Olivia Martin', 'International Grand Prix', '1500m Run', 2, 245.0) # U23 F
    add_result('Daniel Jackson', 'International Grand Prix', '100m Sprint', 1, 10.3) # SEN M
    add_result('Grace Lee', 'International Grand Prix', '800m Run', 1, 128.5) # SEN F

    # Masters Athletics Championship
    add_result('Oliver Scott', 'Masters Athletics Championship', '5000m Run', 1, 980.0) # V35 M
    add_result('Chloe Green', 'Masters Athletics Championship', 'Discus Throw', 1, 35.0) # V40 F
    add_result('Max Adams', 'Masters Athletics Championship', 'Javelin Throw', 2, 40.5) # V45 M
    add_result('Lily Baker', 'Masters Athletics Championship', 'Long Jump', 1, 5.20) # V50 F
    add_result('Jack Turner', 'Masters Athletics Championship', 'High Jump', 1, 1.60) # V55 M
    add_result('Zoe Harris', 'Masters Athletics Championship', '200m Sprint', 1, 30.0) # V60 F

    # Spring Athletics Championship 2026 (Existing, now with new data and consistent age categories)
    add_result('Daniel Jackson', 'Spring Athletics Championship 2026', '200m Sprint', 1, 20.8) # SEN M
    add_result('Grace Lee', 'Spring Athletics Championship 2026', '400m Run', 1, 53.2) # SEN F
    add_result('Ethan Harris', 'Spring Athletics Championship 2026', 'Long Jump', 1, 7.25) # U23 M

    # European Indoor Championships (Existing, now with new data and consistent age categories)
    add_result('Daniel Jackson', 'European Indoor Championships', '100m Sprint', 2, 10.4) # SEN M
    add_result('Olivia Martin', 'European Indoor Championships', 'High Jump', 1, 1.70) # U23 F
    add_result('Max Adams', 'European Indoor Championships', 'Shot Put', 3, 13.0) # V45 M (Example: A master competing in an open event)

    # Summer Open Meet (Existing, now with new data and consistent age categories)
    add_result('Sophia White', 'Summer Open Meet', '200m Sprint', 1, 25.5) # U20 F
    add_result('Oliver Scott', 'Summer Open Meet', '1500m Run', 2, 260.0) # V35 M (Example: A master competing in an open event)
    add_result('Jack Turner', 'Summer Open Meet', 'Pole Vault', 2, 3.50) # V55 M (Example: A master competing in an open event)

    # --- Additional Results ---
    # National Youth Games - More events
    add_result('Leo Garcia', 'National Youth Games', 'Long Jump', 1, 6.10) # U14 M
    add_result('Mia Rodriguez', 'National Youth Games', 'High Jump', 1, 1.55) # U14 F
    add_result('Noah Miller', 'National Youth Games', '800m Run', 1, 118.0) # U16 M
    add_result('Ava Taylor', 'National Youth Games', '3000m Run', 1, 580.0) # U16 F

    # International Grand Prix - More events and athletes
    add_result('Ethan Harris', 'International Grand Prix', 'Long Jump', 2, 7.30) # U23 M
    add_result('Olivia Martin', 'International Grand Prix', 'High Jump', 1, 1.75) # U23 F
    add_result('Daniel Jackson', 'International Grand Prix', '200m Sprint', 1, 20.6) # SEN M
    add_result('Grace Lee', 'International Grand Prix', '400m Run', 2, 53.0) # SEN F

    # Masters Athletics Championship - More events and athletes
    add_result('Oliver Scott', 'Masters Athletics Championship', '10000m Run', 1, 2200.0) # V35 M
    add_result('Chloe Green', 'Masters Athletics Championship', 'Shot Put', 1, 12.8) # V40 F
    add_result('Max Adams', 'Masters Athletics Championship', 'Hammer Throw', 1, 48.0) # V45 M
    add_result('Lily Baker', 'Masters Athletics Championship', '100m Sprint', 1, 14.5) # V50 F
    add_result('Jack Turner', 'Masters Athletics Championship', 'Pole Vault', 1, 3.60) # V55 M
    add_result('Zoe Harris', 'Masters Athletics Championship', 'Triple Jump', 1, 9.50) # V60 F

    # Spring Athletics Championship 2026 - Additional
    add_result('Olivia Martin', 'Spring Athletics Championship 2026', '1500m Run', 1, 240.0) # U23 F
    add_result('Max Adams', 'Spring Athletics Championship 2026', 'Javelin Throw', 1, 46.0) # V45 M
    add_result('Sophia White', 'Spring Athletics Championship 2026', '100m Sprint', 3, 13.2) # U20 F

    # European Indoor Championships - Additional
    add_result('Grace Lee', 'European Indoor Championships', '800m Run', 1, 127.0) # SEN F
    add_result('Oliver Scott', 'European Indoor Championships', '5000m Run', 2, 985.0) # V35 M
    add_result('Jack Turner', 'European Indoor Championships', 'High Jump', 1, 1.65) # V55 M

    # Summer Open Meet - Additional
    add_result('Daniel Jackson', 'Summer Open Meet', 'Long Jump', 1, 7.40) # SEN M
    add_result('Chloe Green', 'Summer Open Meet', 'Discus Throw', 2, 34.5) # V40 F
    add_result('Leo Garcia', 'Summer Open Meet', '100m Sprint', 2, 12.7) # U14 M
    add_result('Mia Rodriguez', 'Summer Open Meet', '200m Sprint', 1, 27.9) # U14 F


    for result_data in results_data:
        athlete = athletes[result_data['athlete_name']]
        competition = competitions[result_data['competition_name']]
        discipline = disciplines[result_data['discipline_name']]
        age_category = age_categories[result_data['age_category']] # Use the determined key

        result = Results.objects.create(
            athlete=athlete,
            competition=competition,
            discipline=discipline,
            age_category=age_category,
            position=result_data['position'],
            result_value=result_data['result_value'],
            result_date=competition.start_date,
        )
        print(f"  ✓ Created result: {result_data['athlete_name']} - {result_data['discipline_name']} ({result_data['age_category'][0]} {result_data['age_category'][1]})")

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


if __name__ == '__main__':
    try:
        load_data()
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        import traceback

        traceback.print_exc()