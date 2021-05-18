
from django.views.generic.base import View
from auctions.models import Listing, Bid, Comment,  Watchlist
from django.urls import path


from . import views

from .views import  ListingCreate, WL_DeleteView


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("listing/<int:id>/", views.listing, name="listing"),    
    path("listingform", ListingCreate.as_view(), name="listingform"), 
    path("<int:id>/delete/", WL_DeleteView.as_view(), name="delete"),   

    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:id>/add_watchlist/", views.add_watchlist,  name="add_watchlist"),   
    path("categories_link", views.categories_link, name="categories_link"),
    path("category_view/<str:category>/", views.category_view, name="category_view"),
    path("close_listing/<int:id>/", views.close_listing, name="close_listing")
    
]