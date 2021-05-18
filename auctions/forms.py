from django.db.models import fields
from django.forms import ModelForm, widgets
from .models import Comment, Listing, Bid
from django import forms 
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


# Made this form to apply form-control 
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['user', 'winner', 'highest_bid', 'inwatchlist', 'datetime', 'active']
        widgets = {
            'description':forms.Textarea(attrs={'rows':4})
        }
       
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('highest_bid',)
        widgets = {
            'highest_bid': forms.NumberInput(attrs={'class':'form-control'}),             
        }
        labels = {
            'highest_bid': '', # This way you hidde the label of the input field
        }
        help_texts = {
            'name': _('Place your bid here.'),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        localized_fields = ('text',)        
        widgets = {
            'text':forms.Textarea(attrs={'class':'form-control', 'rows': '3' })
        }
        labels = {
            'text': '',
        }
