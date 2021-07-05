from django.contrib import admin

from .models import Bid, Category, Image, Listing, User, Watchlist


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "type")

admin.site.register(Bid)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Watchlist)