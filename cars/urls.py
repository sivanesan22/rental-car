from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/book/', views.booking_create, name='booking_create'),
    path('booking/<int:booking_id>/confirm/', views.booking_confirm, name='booking_confirm'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('cars/<int:car_id>/review/', views.post_review, name='post_review'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
]
