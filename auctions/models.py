from abc import abstractclassmethod
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import BooleanField, DateTimeField, FloatField, URLField
from django.http import request
from django.shortcuts import render
from django.urls.base import reverse
from django.utils import tree
from django.utils.timezone import activate, datetime

from django.conf import settings
from django.db.models.fields import related
from django.db.models.fields.related import OneToOneField, ForeignKey




class User(AbstractUser):
    pass


CHOOSE_CATEGORY = (
    ('automotive','Automotive'),
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
)


class Listing(models.Model):    
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='owner')
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='winner')
    item_name = models.CharField(max_length=50, null=True)
    picture_url = models.URLField(blank=True)
    description = models.TextField(max_length=50)
    starting_bid = models.PositiveIntegerField(default=None)    
    highest_bid = models.PositiveIntegerField( default=None)      
    category = models.CharField(max_length=50, choices=CHOOSE_CATEGORY, blank=True)
    active = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True) 

 
    def __str__(self):
        return f"{self.item_name}"

    def get_absolute_url(self):
        return reverse('listing', args=[str(self.id)])
    
        
    
class Bid(models.Model):
    winner = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids', default=None)    
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=None)  
    final_bid = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True )  
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listing} is now {self.highest_bid } worth." 

    def get_absolute_url(self):
        return reverse('bid', args=['name'])


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    text = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        
    
    def __str__(self):
        return f'Comment by {self.user} on {self.listing}'


class Watchlist(models.Model):
    itemid = models.IntegerField(default=None)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='wl_items', default=None)
    wl_owner =  models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    picture_url = models.URLField(default=False)
    active = models.BooleanField(default=True)
   
    
    def __str__(self):
        return f"{self.wl_owner}'s Watchlist"

    def get_absolute_url(self):
        return reverse('watchlist', args=[str(self.watchlist)])
    
   





   