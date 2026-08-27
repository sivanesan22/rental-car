from django import forms
from django.contrib.auth.models import User
from .models import Booking, Review

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'pickup_location', 'dropoff_location']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'id': 'booking-start-date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'id': 'booking-end-date'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Heathrow Airport'}),
            'dropoff_location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Heathrow Airport'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date.")
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-input'}, choices=[(i, f"{i} Stars") for i in range(5, 0, -1)]),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Write your review here...'}),
        }


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
