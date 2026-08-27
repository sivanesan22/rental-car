from django.contrib import admin
from .models import CarCategory, Car, Booking, Review

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'category', 'daily_rate', 'transmission', 'fuel_type', 'is_available')
    list_filter = ('is_available', 'category', 'transmission', 'fuel_type')
    search_fields = ('make', 'model', 'registration_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'start_date', 'end_date', 'total_price', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('user__username', 'car__make', 'car__model')
    actions = ['confirm_booking', 'cancel_booking']

    def confirm_booking(self, request, queryset):
        queryset.update(status='Confirmed')
    confirm_booking.short_description = "Mark selected bookings as Confirmed"

    def cancel_booking(self, request, queryset):
        queryset.update(status='Cancelled')
    cancel_booking.short_description = "Mark selected bookings as Cancelled"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'car__make', 'car__model', 'comment')

