from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.db.models import Max
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .models import User, listing, price, comment

class ListingForm(ModelForm):
    class Meta: 
        model = listing
        fields = ['title', 'description', 'image', 'starting_price', 'category']
        widgets = {
            'starting_price': forms.NumberInput(attrs={'step': 0.25}),
        }

class PriceForm(forms.ModelForm):
    class Meta:
        model = price
        fields = ['bid']
        widgets = {
            'bid': forms.NumberInput(attrs={'step': 0.25}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = comment 
        fields = ['comments']


def index(request):
    return render(request, "auctions/index.html", {
        "listings": listing.objects.all()
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

@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        creator = User.objects.get(username=request.user.username)
        f = ListingForm(request.POST, request.FILES)
        new_listing = f.save(commit=False)
        new_listing.save()
        creator.owner = new_listing
        creator.save()
    return render(request, "auctions/create.html", {
        "form": ListingForm(),
    })

@login_required(login_url='/login')
def item_page(request, listing_id):
    l = listing.objects.get(pk=listing_id)
    b = price.objects.filter(item=l)
    hb = b.aggregate(Max('bid'))
    coms = l.opinions.all()
    if hb.get('bid__max') is not None:
        high_bid = float(hb.get('bid__max'))
    else:
        high_bid = hb
    user = User.objects.get(username=request.user.username)
    watching = user.watching.all()
    if request.method == "POST":
        if 'add' in request.POST:
            user.watching.add(listing_id)
        elif 'remove' in request.POST:
            user.watching.remove(listing_id)
        elif 'close' in request.POST:
            l.closed = True 
            l.save()
            highest = price.objects.get(bid=high_bid)
            won = highest.bidder 
            won.winner = l
            won.save()
        elif 'content' in request.POST:
            c = comment(comments=request.POST['content'], for_sale=l)
            c.save()
        else:
            f = PriceForm(request.POST)
            new_bid = f.save(commit=False)
            if hb.get('bid__max') is not None: 
                if high_bid > new_bid.bid:
                    raise ValidationError("Price must be greater than current high bid")
            new_bid.bidder = user
            new_bid.item = l
            new_bid.save()
    return render(request, "auctions/listing.html", {
        "listing": l,
        "bid": PriceForm(),
        "price": high_bid,
        "watching": watching,
        "user": user,
        "comments": coms
     })

@login_required(login_url='/login')
def watchlist(request):
    watcher = User.objects.get(username=request.user.username)
    watching = watcher.watching.all()
    return render(request, "auctions/watchlist.html", {
        "watching": watching
    })

def categories(request):
    cat = listing.CATEGORIES
    return render(request, "auctions/categories.html", {
        "categories": cat
    })

def title(request, category_title):
    category_listings = listing.objects.filter(category=category_title)
    return render(request, "auctions/title.html", {
        "category_listings": category_listings
    })


