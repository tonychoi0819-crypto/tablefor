from django.db import models
from django.conf import settings

class SiteSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    description = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'site_settings'
        verbose_name_plural = 'Site Settings'
    def __str__(self):
        return self.key

class PageView(models.Model):
    url = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'page_view'
        ordering = ['-created_at']
