from django.urls import path
from apps.bookings.views import BookingCreateView, MyBookingsView, BookingCancelView
from django.views.generic import ListView, DetailView
from .models import Booking
app_name = 'bookings'
urlpatterns = [
    path('', MyBookingsView.as_view(), name='my_bookings'),
    path('new/<int:restaurant_id>/', BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>/', DetailView.as_view(model=Booking, template_name='bookings/detail.html'), name='booking_detail'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking_cancel'),
]
