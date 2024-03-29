from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Category(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type}"


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class Listing(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    start_bid = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(
        Category,
        related_name="listings"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )
    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.id}: {self.title} ({self.start_bid})"


class Bid(models.Model):
    bid = models.DecimalField(
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )

    def __str__(self):
        return f"Listing: {self.listing} Current Bid: {self.bid} User: {self.user}"


class Image(models.Model):
    listing = models.OneToOneField(
        Listing, 
        on_delete=models.CASCADE
    )
    image_url = models.URLField()

    def __str__(self):
        return f"{self.listing}: {self.image_url}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        default=None
    )

    def __str__(self):
        return f"User: {self.user} Listing: {self.listing}"

class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(default=timezone.now)
