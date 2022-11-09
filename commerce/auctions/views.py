from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Category
from .forms import AuctionForm

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

def auction(request, auction_title):
    existing_titles = list(auction.title for auction in Auction.objects.all())
    if auction_title.upper() in list(map(str.upper,existing_titles)):
        return render(request, "auctions/auction.html",{
            "auction": Auction.objects.get(title__iexact=auction_title)
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
            new_auction = Auction(title=title,description=description,starting_bid=starting_bid, imageURL=imageURL, seller=seller)
            new_auction.save()
            new_auction.category.add(*category_list)
            
    form = AuctionForm()    
    return render(request, "auctions/create.html",{
        "form": form
    })

def watchlist(request):
    
    return render(request, "auctions/watchlist.html")
