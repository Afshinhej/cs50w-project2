from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Category, Bid
from .forms import AuctionForm, BidingForm, WatcllistForm

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
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

def auction(request, auction_pk):
    caution = None
    if request.method == "POST":
        if "is_it_watchlist" in request.POST:
            request.user.watchlist.add(Auction.objects.get(pk=auction_pk))                
        elif "bid" in request.POST:
            form = BidingForm(request.POST)
            if form.is_valid():
                bid = float(form.cleaned_data["bid"])
                purchaser = request.user
                item_pk = request.POST['item_pk']
                item = Auction.objects.get(pk=item_pk)
                if item.max_bid()<bid:
                    Bid(bid=bid, purchaser=purchaser, item=item).save()
                else:
                    caution = "The bid must be higher than the current price!"
        else:
            request.user.watchlist.remove(Auction.objects.get(pk=auction_pk))
    if Auction.objects.get(pk=auction_pk) in request.user.watchlist.all():
        watcllistForm = WatcllistForm({'is_it_watchlist': ['on']})
    else:
        watcllistForm = WatcllistForm()
    
    existing_pk = list(auction.pk for auction in Auction.objects.all())
    if auction_pk in existing_pk:
        auction = Auction.objects.get(pk=auction_pk)
        return render(request, "auctions/auction.html",{
            "auction": auction,
            "form": BidingForm,
            "price": max(auction.max_bid(), auction.starting_bid),
            "count_bid": auction.count_bid(),
            "watcllistForm": watcllistForm,
            "caution": caution
        })
    return render(request, "auctions/auction.html",{
        'message':"No data available!"
    })

def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            category_names = form.cleaned_data["category"]
            category_list = list(Category.objects.get(name = category_name).id for category_name in category_names)
            imageURL = form.cleaned_data["imageURL"]
            seller = request.user
            new_auction = Auction(title=title, description=description, starting_bid=starting_bid, imageURL=imageURL, seller=seller)
            new_auction.save()
            new_auction.category.add(*category_list)
            
    form = AuctionForm()
    return render(request, "auctions/create.html",{
        "form": form
    })

def watchlist(request):
    if request.method == "GET":
        return render(request, "auctions/watchlist.html",{
            "auctions":request.user.watchlist.all()
        })

def categoryindex(request):
    return render(request, "auctions/categoryindex.html",{
        "categorys": Category.objects.all()
    })
    
def category(request, category_pk):
    return render(request, "auctions/category.html",{
        "category": Category.objects.get(pk=category_pk),
        "auctions": Auction.objects.filter(category=Category.objects.get(pk=category_pk))
    })