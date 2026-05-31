from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.restaurants.models import District, Cuisine, Tag, Restaurant, MenuItem
from apps.reviews.models import Review
from apps.deals.models import Deal
from apps.accounts.models import User
from django.utils import timezone
from datetime import timedelta, date
import random

class Command(BaseCommand):
    help = 'Seed comprehensive HK restaurant data'

    def handle(self, *args, **options):
        self.stdout.write("Seeding...")
