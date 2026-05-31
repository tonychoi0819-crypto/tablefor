from django.db import models

class Restaurant(models.Model):
    CUISINE_CHOICES = [
        ('chinese', 'Chinese'), ('western', 'Western'), ('japanese', 'Japanese'),
        ('korean', 'Korean'), ('thai', 'Thai'), ('vietnamese', 'Vietnamese'),
        ('indian', 'Indian'), ('italian', 'Italian'), ('french', 'French'),
        ('fusion', 'Fusion'), ('cafe', 'Cafe'), ('bakery', 'Bakery'),
        ('fast_food', 'Fast Food'), ('seafood', 'Seafood'), ('other', 'Other'),
    ]
    PRICE_CHOICES = [('$', 'Budget'), ('$$', 'Moderate'), ('$$$', 'Expensive'), ('$$$$', 'Fine Dining')]
    name_en = models.CharField(max_length=200)
    name_zh = models.CharField(max_length=200, blank=True)
    cuisine_type = models.CharField(max_length=20, choices=CUISINE_CHOICES, default='other')
    price_range = models.CharField(max_length=4, choices=PRICE_CHOICES, default='$$')
    address = models.TextField()
    district = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)
    opening_hours = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant'
        ordering = ['name_en']

    def __str__(self):
        return self.name_en
