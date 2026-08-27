import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cars.models import CarCategory, Car, Review
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with initial car categories, cars, reviews, and a superuser.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # 1. Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@rentacar.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully with password "admin123"'))
        else:
            self.stdout.write('Superuser "admin" already exists.')

        # 2. Create Categories
        categories_data = [
            {
                'name': 'Electric',
                'description': 'Premium electric vehicles with cutting-edge technology and zero emissions.',
                'image': 'categories/electric.jpg'
            },
            {
                'name': 'Sports',
                'description': 'High-performance sports cars that deliver thrilling speed and precision handling.',
                'image': 'categories/sports.jpg'
            },
            {
                'name': 'SUVs',
                'description': 'Spacious and rugged SUVs designed for family comfort and off-road adventures.',
                'image': 'categories/suv.jpg'
            },
            {
                'name': 'Luxury',
                'description': 'Elite passenger vehicles boasting unparalleled comfort, style, and prestige.',
                'image': 'categories/luxury.jpg'
            }
        ]

        categories = {}
        for cat_info in categories_data:
            cat, created = CarCategory.objects.get_or_create(
                slug=slugify(cat_info['name']),
                defaults={
                    'name': cat_info['name'],
                    'description': cat_info['description'],
                    'image': cat_info['image']
                }
            )
            categories[cat_info['name']] = cat
            if created:
                self.stdout.write(f"Created category: {cat.name}")

        # 3. Create Cars
        cars_data = [
            {
                'make': 'Tesla',
                'model': 'Model S Plaid',
                'year': 2024,
                'category': categories['Electric'],
                'transmission': 'Automatic',
                'fuel_type': 'Electric',
                'daily_rate': 149.00,
                'seats': 5,
                'luggage': 3,
                'ac': True,
                'registration_number': 'TSLA-PLAID',
                'image': 'cars/tesla.jpg',
                'is_available': True
            },
            {
                'make': 'Porsche',
                'model': '911 Carrera S',
                'year': 2023,
                'category': categories['Sports'],
                'transmission': 'Automatic',
                'fuel_type': 'Petrol',
                'daily_rate': 249.00,
                'seats': 4,
                'luggage': 1,
                'ac': True,
                'registration_number': '911-PORSCHE',
                'image': 'cars/porsche.jpg',
                'is_available': True
            },
            {
                'make': 'BMW',
                'model': 'M4 Competition',
                'year': 2024,
                'category': categories['Sports'],
                'transmission': 'Automatic',
                'fuel_type': 'Petrol',
                'daily_rate': 179.00,
                'seats': 4,
                'luggage': 2,
                'ac': True,
                'registration_number': 'BMW-M4COMP',
                'image': 'cars/bmw.jpg',
                'is_available': True
            },
            {
                'make': 'Land Rover',
                'model': 'Range Rover Sport',
                'year': 2023,
                'category': categories['SUVs'],
                'transmission': 'Automatic',
                'fuel_type': 'Hybrid',
                'daily_rate': 199.00,
                'seats': 5,
                'luggage': 4,
                'ac': True,
                'registration_number': 'RR-SPORT',
                'image': 'cars/rover.jpg',
                'is_available': True
            },
            {
                'make': 'Mercedes-Benz',
                'model': 'S-Class',
                'year': 2024,
                'category': categories['Luxury'],
                'transmission': 'Automatic',
                'fuel_type': 'Petrol',
                'daily_rate': 299.00,
                'seats': 5,
                'luggage': 3,
                'ac': True,
                'registration_number': 'MB-S580',
                'image': 'cars/mercedes.jpg',
                'is_available': True
            },
            {
                'make': 'Hyundai',
                'model': 'Ioniq 5',
                'year': 2024,
                'category': categories['Electric'],
                'transmission': 'Automatic',
                'fuel_type': 'Electric',
                'daily_rate': 99.00,
                'seats': 5,
                'luggage': 3,
                'ac': True,
                'registration_number': 'HYU-IONIQ5',
                'image': 'cars/ioniq.jpg',
                'is_available': True
            }
        ]

        for car_info in cars_data:
            car, created = Car.objects.get_or_create(
                registration_number=car_info['registration_number'],
                defaults=car_info
            )
            if created:
                self.stdout.write(f"Created car: {car}")

                # Create seed reviews for this car
                # Create a temporary dummy user for the review if needed
                review_user, _ = User.objects.get_or_create(
                    username='guest_driver',
                    defaults={'email': 'guest@driver.com'}
                )
                review_user.set_password('guest123')
                review_user.save()

                Review.objects.get_or_create(
                    user=review_user,
                    car=car,
                    defaults={
                        'rating': 5 if car.make in ['Porsche', 'Tesla', 'Mercedes-Benz'] else 4,
                        'comment': f"Amazing drive! The {car.make} {car.model} exceeded all expectations. Extremely clean and fast."
                    }
                )

        self.stdout.write(self.style.SUCCESS('Database seeding finished successfully.'))
