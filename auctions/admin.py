from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Listing, Bid, Comment, User, Watchlist
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'winner',
        'item_name', 
        'description',
        'starting_bid',
        'highest_bid', 
        'category',
        'datetime', 
        'active')



class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'text', 'created', 'active')
    list_filter = ('created','active')



class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('itemid', 'wl_owner', 'item', 'picture_url')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'winner', 'listing', 'highest_bid', 'final_bid', 'active')    



admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(User, UserAdmin)
