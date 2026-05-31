from django.db import models

class Deal(models.Model):
    DEAL_TYPE_CHOICES = [('discount', 'Discount'), ('set_menu', 'Set Menu'), ('free_item', 'Free Item'), ('cashback', 'Cashback'), ('happy_hour', 'Happy Hour')]
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='deals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES)
    discount_percent = models.PositiveSmallIntegerField(null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    min_spending = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    terms = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    usage_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'deal'
        ordering = ['-start_date']
    def __str__(self):
        return f'{self.title} - {self.restaurant.name_en}'
    @property
    def is_current(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
