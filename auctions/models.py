from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    start_bid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.id}: {self.title} ({self.start_bid})"


class User(AbstractUser):
    pass


# OneToOne associations
class Image(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.listing}: {self.image_url}"