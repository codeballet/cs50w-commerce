from django.contrib import admin

from .models import Category, Image, Listing, User


# Register your models here.
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Listing)
admin.site.register(User)