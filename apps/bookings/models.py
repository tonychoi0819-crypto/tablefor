from django.db import models
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('no_show', 'No Show'), ('completed', 'Completed')]
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    party_size = models.PositiveSmallIntegerField(default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'booking'
        ordering = ['-date', '-time']
    def __str__(self):
        return f'{self.confirmation_code} - {self.restaurant.name_en} ({self.date} {self.time})'

class Waitlist(models.Model):
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='waitlist')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waitlist_entries')
    date = models.DateField()
    party_size = models.PositiveSmallIntegerField(default=2)
    estimated_wait_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'waitlist'
        ordering = ['created_at']
