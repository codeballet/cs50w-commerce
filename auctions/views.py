from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .forms import BidForm, ListingForm
from .models import Bid, Category, Image, Listing, User


def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "all_listings": all_listings
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.order_by('type')
    })


def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            l = Listing(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                start_bid = form.cleaned_data['start_bid'],
            )
            l.save()

            for category in form.cleaned_data["categories"]:
                print(f"Category: {category}")
                c = Category.objects.get(type=category)
                l.categories.add(c)

            i = Image(listing = l, image_url = form.cleaned_data['image_url'])
            i.save()

            return HttpResponseRedirect(reverse("index"))

    form = ListingForm()
    return render(request, "auctions/create.html", {
        "form": form,
    })


def listing(request, listing_id):
    message = ''

    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            l = Listing.objects.get(pk=listing_id)
            bid = bid_form.cleaned_data['current_bid']

            # Check if bid is smaller or equal to starting bid
            # or current bid
            start = l.start_bid
            current = l.bid_set.aggregate(Max('current_bid'))

            if bid <= start or bid <= current['current_bid__max']:
                return render(request, "auctions/listing.html", {
                    "bid_form": bid_form,
                    "listing": l,
                    "error": "Your must bid higher."
                })

            b = Bid(
                current_bid = bid_form.cleaned_data['current_bid']
            )
            b.listing = l
            b.save()

            message = "Your bid was successful."

    bid_form = BidForm()
    l = Listing.objects.filter(pk = listing_id).first()

    # Check if there is a current_bid
    if l.bid_set:
        current = l.bid_set.aggregate(Max('current_bid'))
        current_price = current['current_bid__max']
    else:
        current_price = l.start_bid
    return render(request, "auctions/listing.html", {
        "bid_form": bid_form,
        "listing": l,
        "current_price": current_price,
        "message": message
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
