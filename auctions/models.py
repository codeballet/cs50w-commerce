from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Base classes
class Category(models.Model):
    ELECTRONICS = 'electronics'
    FASHION = 'fashion'
    HOME = 'home'
    OTHER = 'other'
    TOYS = 'toys'
    CATEGORIES = [
        (ELECTRONICS, 'Electronics'),
        (FASHION, 'Fashion'),
        (HOME, 'Home'),
        (OTHER, 'Other'),
        (TOYS, 'Toys')
    ]

    type = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default=OTHER
    )


class Listing(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    start_bid = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}: {self.title} ({self.start_bid})"


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


# OneToOne associations
class Image(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.listing}: {self.image_url}"