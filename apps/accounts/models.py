from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [('diner', 'Diner'), ('owner', 'Restaurant Owner'), ('admin', 'Admin')]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='diner')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    district = models.CharField(max_length=100, blank=True)
    is_verified_diner = models.BooleanField(default=False)
    review_count = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_user'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def update_review_count(self):
        from apps.reviews.models import Review
        self.review_count = Review.objects.filter(user=self, is_published=True).count()
        self.save(update_fields=[chr(114) + chr(101) + chr(118) + chr(105) + chr(101) + chr(119) + chr(95) + chr(99) + chr(111) + chr(117) + chr(110) + chr(116)])
