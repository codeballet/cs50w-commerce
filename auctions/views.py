from typing import List
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .forms import BidForm, ListingForm, CommentForm
from .models import Bid, Category, Image, Listing, User, Watchlist, Comment


def index(request):
    all_listings = Listing.objects.all()
    items = []

    for listing in all_listings:
        last_bid = Bid.objects.filter(listing=listing).order_by('-timestamp').first()
        if last_bid:
            price = last_bid.bid
        else:
            price = listing.start_bid

        image = Image.objects.filter(listing=listing).first()
        if image:
            image = image.image_url
            
        items.append({
            'title': listing.title,
            'time': listing.timestamp,
            'price': price,
            'active': listing.active,
            'id': listing.id,
            'image': image,
            'description': listing.description
        })

    return render(request, "auctions/index.html", {
        "items": items
    })


def categories(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "auctions/categories.html", {
        "categories": Category.objects.order_by('type')
    })

def category(request, category_id):
    c = Category.objects.get(pk=category_id)
    c_listings = Listing.objects.filter(
        categories = c.id, 
        active = True
    )

    # get price for listings
    for listing in c_listings:
        last_bid = Bid.objects.filter(listing=listing).order_by('-timestamp').first()
        if last_bid:
            price = last_bid.bid
        else:
            price = listing.start_bid

    return render(request, "auctions/category.html", {
        "c_listings": c_listings,
        "category": c.type,
        "price": price
    })


def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            l = Listing(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                start_bid = form.cleaned_data['start_bid'],
                user_id = request.user.id
            )
            l.save()

            for category in form.cleaned_data["categories"]:
                print(f"Category: {category}")
                c = Category.objects.get(type=category)
                l.categories.add(c)

            image = form.cleaned_data['image_url']
            if image:
                i = Image(listing = l, image_url = image)
                i.save()

            return HttpResponseRedirect(reverse("index"))

    form = ListingForm()
    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
        "form": form,
        "categories": categories
    })


def listing(request, listing_id):
    message = ''

    if request.user.is_authenticated:
        watched = Watchlist.objects.filter(user=request.user, listing=listing_id).first()
    else:
        watched = None

    l = Listing.objects.filter(pk=listing_id).first()
    
    # Get the forms
    bid_form = BidForm()
    comment_form = CommentForm()

    # Check if there is a current_bid
    if l.bid_set:
        current = l.bid_set.aggregate(Max('bid'))
        current_price = current['bid__max']
    else:
        current_price = l.start_bid

    # Get comments for item
    comments = Comment.objects.filter(listing = l)

    # get last bid and check if it is the current user
    last_bid = Bid.objects.filter(listing=listing_id).order_by('-timestamp').first()
    if last_bid:
        current_user_bid = last_bid.user == request.user
    else:
        current_user_bid = False

    # check how many bids has been made
    bid_count = Bid.objects.filter(listing=listing_id).count()

    # for POST requests
    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            bid = bid_form.cleaned_data['bid']

            # Check if bid is smaller or equal to starting bid
            # or current bid
            start = l.start_bid
            current_list = l.bid_set.aggregate(Max('bid'))
            current = current_list['bid__max']

            if not current:
                current = 0

            if bid < start or bid <= current:
                if current == 0:
                    current = None
                return render(request, "auctions/listing.html", {
                    "bid_form": bid_form,
                    "comment_form": comment_form,
                    "listing": l,
                    "current_price": current_price,
                    "message": message,
                    "watched": watched,
                    "last_bid": last_bid,
                    "comments": comments,
                    "categories": l.categories.all(),
                    "bid_count": bid_count,
                    "error": "Your must bid higher.",
                    "current_user_bid": current_user_bid
                })

            b = Bid(
                bid = bid_form.cleaned_data['bid']
            )
            b.listing = l
            b.user = request.user
            b.save()

            message = "Your bid was successful."

    return render(request, "auctions/listing.html", {
        "bid_form": bid_form,
        "comment_form": comment_form,
        "listing": l,
        "current_price": current_price,
        "message": message,
        "watched": watched,
        "last_bid": last_bid,
        "comments": comments,
        "categories": l.categories.all(),
        "bid_count": bid_count,
        "current_user_bid": current_user_bid
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def watch(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        listing = Listing.objects.filter(pk = listing_id).first()
        if request.POST["watch"] == "Add to Watchlist":
            watch = Watchlist(user=request.user, listing=listing)
            watch.save()
        if request.POST["watch"] == "Remove from Watchlist":
            watch = Watchlist.objects.filter(user=request.user, listing=listing).first()
            watch.delete()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    listings = Listing.objects.filter(watchlist__user=request.user)

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def close(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        listing = Listing.objects.filter(pk = listing_id).first()
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def comment(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        print("Inside the comment function")
        listing = Listing.objects.filter(pk = listing_id).first()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            print(f"Form checked, about to save to database")
            new_comment = Comment(
                comment = comment_form.cleaned_data['comment'],
                user = request.user,
                listing = listing
            )
            new_comment.save()
            print(f"Comment Saved to database")
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))