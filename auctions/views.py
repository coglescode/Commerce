
from django.utils import tree
from django.utils.translation import activate
from django.views.generic.edit import FormMixin, UpdateView
import auctions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.db import IntegrityError
from django.db.models.fields import CommaSeparatedIntegerField, URLField

from django.forms import fields, models, widgets, ModelForm
from django.http import HttpResponse, HttpResponseRedirect, request, response
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy

from .models import CHOOSE_CATEGORY,  User, Listing, Bid, Comment, Watchlist
from django.views.generic import CreateView,  DeleteView
from .forms import BidForm, ListingForm, CommentForm
from django.contrib import messages




    
# My first try with CBV
class ListingCreate(LoginRequiredMixin, CreateView):
        model = Listing       
        success_url = '/'              
        form_class = ListingForm     

        def form_valid(self, form):
            form.instance.user = self.request.user
            form.instance.highest_bid = self.request.POST['starting_bid']
            return super().form_valid(form)


class WL_DeleteView(LoginRequiredMixin, DeleteView):
    model = Watchlist
    template_name = 'auctions/watchlist.html'

    def get_object(self):
        id = self.kwargs.get('id')        
        return get_object_or_404(Watchlist, id=id )

    def get_success_url(self):
        return reverse('watchlist')
        
# Idid try to do more with CBV but I realized I need to fully understand function views before I do the jump 

# Function to place bid and comment on active listings items
def listing(request, id):
    listings = Listing.objects.filter(id=id)
    listing = get_object_or_404(Listing, id=id)
    winner = request.user
    comments = listing.comments.filter(active=True)

    new_bid = []
    new_comment = []

    if request.method == 'POST':
        bid_form = BidForm(request.POST)  
        comment_form = CommentForm(request.POST)   
        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            new_bid.listing = listing
            new_bid.winner = winner
            new_bid.id = id  
            if new_bid.highest_bid > listing.highest_bid:                
                Listing.objects.filter(id=id).update(highest_bid=new_bid.highest_bid)     
                new_bid.save()             
                messages.add_message(request, messages.SUCCESS, "You are leading")              
            else:
                messages.add_message(request, messages.ERROR, "You need to bid more")
        elif comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.listing = listing
            new_comment.save()
            new_comment.user = request.user
            new_comment.save()        
        else:
            return render(request, "auctions/listing_view.html", {              
                "listings":listings,                
                "bid_form":bid_form,
                "comment_form":comment_form
             }) 
                  
    return render(request, "auctions/listing_view.html", {
        "listings":listings,    
        "comments": comments,
        "new_comment": new_comment,
        "new_bid":new_bid,    
        "bid_form":BidForm(),
        "comment_form":CommentForm(),      
    })



def watchlist(request):  
    return render(request, 'auctions/watchlist.html', {
        'wl_items': Watchlist.objects.filter(wl_owner=request.user)
    })


# Function to save the listing in the watchlist database
def add_watchlist(request, id):   
    listing = Listing.objects.get(id=id)
        
    obj, created = Watchlist.objects.get_or_create(   
    itemid = listing.id,
    wl_owner = request.user,    
    item = listing,
    picture_url = listing.picture_url,                     
    )
    return redirect('watchlist')


def categories_link(request):    
    return render(request, 'auctions/categories_link.html', )


# Function to add the requested category in to a list to be shown on a dedicated template for the same category
def category_view(request, category):
    listing = Listing.objects.filter( category=category, active=True)
 
    categories = []

    for x in listing:
        if x not in categories:
            categories.append(x)
        
    return render(request,"auctions/categoryview.html",{
        "categories":categories,
        "listing":listing
    })
    
# Function to close the listing by the creator only
def close_listing(request, id):    
    listing = get_object_or_404(Listing, id=id)
    bid = get_object_or_404(Bid, id=id)
    
    if listing.user == request.user:
        closed_bid = Bid.objects.filter(id=id).update(final_bid=listing.highest_bid, active=False)
        closed_listing = Listing.objects.filter(id=id).update(winner=bid.winner, active=False)
                
        listings = Listing.objects.filter(id=id)
  
        winner = listing.winner
        return render(request, 'auctions/listing_view.html', {
            'listings':listings,  
            'winners':winner,          
            'closed_listing': closed_listing
        })




            #### Course staff code ####  

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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




