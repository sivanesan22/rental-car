from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
import datetime

from .models import CarCategory, Car, Booking, Review
from .forms import BookingForm, ReviewForm, RegisterForm

def home(request):
    categories = CarCategory.objects.all()
    # Fetch top 3 featured cars (highest rates or just premium ones)
    featured_cars = Car.objects.filter(is_available=True)[:3]
    return render(request, 'cars/home.html', {
        'categories': categories,
        'featured_cars': featured_cars
    })


def car_list(request):
    cars = Car.objects.all()
    categories = CarCategory.objects.all()

    # Query filters
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    transmission = request.GET.get('transmission')
    fuel_type = request.GET.get('fuel')
    price_max = request.GET.get('price_max')

    # Apply search query
    if query:
        cars = cars.filter(
            Q(make__icontains=query) | 
            Q(model__icontains=query) | 
            Q(category__name__icontains=query)
        )

    # Filter by category slug
    if category_slug:
        cars = cars.filter(category__slug=category_slug)

    # Filter by transmission
    if transmission in ['Manual', 'Automatic']:
        cars = cars.filter(transmission=transmission)

    # Filter by fuel type
    if fuel_type in ['Electric', 'Hybrid', 'Petrol', 'Diesel']:
        cars = cars.filter(fuel_type=fuel_type)

    # Filter by daily rate
    if price_max:
        try:
            cars = cars.filter(daily_rate__lte=float(price_max))
        except ValueError:
            pass

    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'categories': categories,
        'selected_category': category_slug,
        'selected_transmission': transmission,
        'selected_fuel': fuel_type,
        'selected_price': price_max,
        'query': query
    })


def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    reviews = car.reviews.all()
    booking_form = BookingForm()
    review_form = ReviewForm()

    # Get conflicting booked dates for simple UI warnings/disable options in calendar if needed
    confirmed_bookings = car.bookings.filter(status__in=['Pending', 'Confirmed'])
    disabled_dates = []
    for b in confirmed_bookings:
        curr = b.start_date
        while curr <= b.end_date:
            disabled_dates.append(curr.strftime('%Y-%m-%d'))
            curr += datetime.timedelta(days=1)

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'reviews': reviews,
        'booking_form': booking_form,
        'review_form': review_form,
        'disabled_dates': disabled_dates
    })


@login_required
def booking_create(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            
            # Check for scheduling collisions
            collision = Booking.objects.filter(
                car=car,
                status__in=['Pending', 'Confirmed']
            ).filter(
                Q(start_date__lte=booking.end_date) & Q(end_date__gte=booking.start_date)
            ).exists()

            if collision:
                messages.error(request, "This car is already booked for the selected dates. Please select other dates.")
                return redirect('car_detail', car_id=car.id)

            # Prevent bookings in the past
            if booking.start_date < datetime.date.today():
                messages.error(request, "Pick-up date cannot be in the past.")
                return redirect('car_detail', car_id=car.id)

            # Calculate total cost
            days = (booking.end_date - booking.start_date).days
            days = max(days, 1)  # Minimum 1 day rate
            booking.total_price = car.daily_rate * days
            booking.status = 'Pending'
            booking.save()

            return redirect('booking_confirm', booking_id=booking.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
            return redirect('car_detail', car_id=car.id)

    return redirect('car_detail', car_id=car_id)


@login_required
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'Confirmed'
        booking.save()
        messages.success(request, f"Your booking for the {booking.car} has been confirmed successfully!")
        return redirect('profile_dashboard')

    return render(request, 'cars/booking_confirm.html', {
        'booking': booking
    })


@login_required
def profile_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cars/profile.html', {
        'bookings': bookings
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    # Check if booking is cancelable (not completed or already cancelled, and is in future)
    if booking.status in ['Pending', 'Confirmed']:
        if booking.start_date >= datetime.date.today():
            booking.status = 'Cancelled'
            booking.save()
            messages.success(request, f"Booking #{booking.id} cancelled successfully.")
        else:
            messages.error(request, "Cannot cancel active or past bookings.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
        
    return redirect('profile_dashboard')


@login_required
def post_review(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.car = car
            review.save()
            messages.success(request, "Thank you! Your review has been posted.")
        else:
            messages.error(request, "Failed to submit review. Please check your rating.")
    
    return redirect('car_detail', car_id=car.id)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Log the user in
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Antigravity Car Rentals.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegisterForm()
        
    return render(request, 'cars/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'cars/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

