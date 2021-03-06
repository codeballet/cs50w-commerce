from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Category(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type}"


class Listing(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    start_bid = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(
        Category,
        related_name="listings"
    )

    def __str__(self):
        return f"{self.id}: {self.title} ({self.start_bid})"


class User(AbstractUser):
    listings = models.ManyToManyField(
        Listing,
        related_name="users"
    )

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


# Association tables
class Bid(models.Model):
    current_bid = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=None
    )
    timestamp = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        default=None
    )


class Image(models.Model):
    listing = models.OneToOneField(
        Listing, 
        on_delete=models.CASCADE
    )
    image_url = models.URLField()

    def __str__(self):
        return f"{self.listing}: {self.image_url}"