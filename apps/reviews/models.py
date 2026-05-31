from django.db import models
from django.conf import settings

class Review(models.Model):
    MEAL_CHOICES = [('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('brunch', 'Brunch'), ('tea', 'Afternoon Tea'), ('supper', 'Supper')]
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, blank=True)
    visit_date = models.DateField(null=True, blank=True)
    party_size = models.PositiveSmallIntegerField(null=True, blank=True)
    spending_per_head = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    owner_response = models.TextField(blank=True)
    owner_responded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'review'
        ordering = ['-created_at']
        unique_together = ['user', 'restaurant']
    def __str__(self):
        return self.user.username + ' - ' + self.restaurant.name_en + ' (' + str(self.rating) + ')'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.restaurant.update_rating()
        self.user.update_review_count()

class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='reviews/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'review_photo'
        ordering = ['created_at']

class ReviewHelpful(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'review_helpful'
        unique_together = ['review', 'user']
