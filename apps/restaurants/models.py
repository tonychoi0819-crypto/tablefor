from django.db import models
from django.conf import settings

class District(models.Model):
    REGION_CHOICES = [('HK', 'Hong Kong Island'), ('KLN', 'Kowloon'), ('NT', 'New Territories'), ('Macau', 'Macau')]
    name_en = models.CharField(max_length=100)
    name_tc = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    class Meta:
        db_table = 'restaurant_district'
        ordering = ['region', 'name_en']
    def __str__(self):
        return self.name_en

class Cuisine(models.Model):
    name_en = models.CharField(max_length=100)
    name_tc = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'restaurant_cuisine'
        verbose_name_plural = 'Cuisines'
        ordering = ['name_en']
    def __str__(self):
        return self.name_en

class Tag(models.Model):
    TAG_TYPE_CHOICES = [('dietary', 'Dietary'), ('amenity', 'Amenity'), ('atmosphere', 'Atmosphere'), ('meal', 'Meal Type')]
    name_en = models.CharField(max_length=100)
    name_tc = models.CharField(max_length=100, blank=True)
    tag_type = models.CharField(max_length=20, choices=TAG_TYPE_CHOICES)
    class Meta:
        db_table = 'restaurant_tag'
        ordering = ['tag_type', 'name_en']
    def __str__(self):
        return self.name_en

class Restaurant(models.Model):
    PRICE_CHOICES = [('$', 'Under $50'), ('$$', '$50-100'), ('$$$', '$100-200'), ('$$$$', '$200-500'), ('$$$$$', '$500+')]
    STATUS_CHOICES = [('pending', 'Pending'), ('verified', 'Verified'), ('claimed', 'Claimed by Owner'), ('closed', 'Permanently Closed')]
    name_en = models.CharField(max_length=200)
    name_tc = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='restaurants')
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants', blank=True)
    tags = models.ManyToManyField(Tag, related_name='restaurants', blank=True)
    address_en = models.TextField()
    address_tc = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    price_range = models.CharField(max_length=5, choices=PRICE_CHOICES, default='$$')
    opening_hours = models.JSONField(default=dict, blank=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)
    photo_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    claimed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_restaurants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'restaurant'
        ordering = ['-avg_rating', '-review_count']
    def __str__(self):
        return self.name_en
    def update_rating(self):
        from apps.reviews.models import Review
        reviews = Review.objects.filter(restaurant=self, is_published=True)
        self.review_count = reviews.count()
        if self.review_count > 0:
            total = sum(r.rating for r in reviews)
            self.avg_rating = round(total / self.review_count, 2)
        else:
            self.avg_rating = 0
        self.save(update_fields=['avg_rating', 'review_count'])

class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='restaurants/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'restaurant_photo'
        ordering = ['-is_primary', '-created_at']
    def __str__(self):
        return self.restaurant.name_en + ' photo'

class MenuItem(models.Model):
    CATEGORY_CHOICES = [('appetizer', 'Appetizer'), ('main', 'Main Course'), ('dessert', 'Dessert'), ('drink', 'Drink'), ('side', 'Side'), ('special', 'Chef Special')]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name_en = models.CharField(max_length=200)
    name_tc = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')
    dietary_tags = models.ManyToManyField(Tag, blank=True, related_name='menu_items')
    photo = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'menu_item'
        ordering = ['category', 'name_en']
    def __str__(self):
        return self.name_en + ' (' + self.restaurant.name_en + ')'
