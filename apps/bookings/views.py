from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Booking
from apps.restaurants.models import Restaurant
import secrets

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['date', 'time', 'party_size', 'special_requests']
    template_name = 'bookings/form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        form.instance.confirmation_code = 'TB' + secrets.token_hex(4).upper()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('bookings:my_bookings')

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('restaurant')

class BookingCancelView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = []
    template_name = 'bookings/cancel.html'
    def form_valid(self, form):
        self.object.status = 'cancelled'
        self.object.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('bookings:my_bookings')
