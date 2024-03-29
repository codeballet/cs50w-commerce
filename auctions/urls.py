from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/watch", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/comment", views.comment, name="comment")
]
