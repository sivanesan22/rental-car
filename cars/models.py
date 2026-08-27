from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Car Categories"

    def __str__(self):
        return self.name


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]
    FUEL_CHOICES = [
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
    ]

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, related_name='cars')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    seats = models.PositiveIntegerField(default=5)
    luggage = models.PositiveIntegerField(default=2)
    ac = models.BooleanField(default=True)
    registration_number = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

    @property
    def review_count(self):
        return self.reviews.count()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} ({self.car})"

    @property
    def duration_days(self):
        delta = self.end_date - self.start_date
        return max(delta.days, 1)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} on {self.car} - Rating: {self.rating}"

