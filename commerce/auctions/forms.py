from django import forms
from .models import Category, Comment

categorys = list(category for category in Category.objects.all())
category_choices = []
for _ in categorys:
    category_choices.append((_,str(_.name)))

class AuctionForm(forms.Form):
    title = forms.CharField(label='Auction title', max_length=64)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    starting_bid = forms.FloatField()
    category = forms.MultipleChoiceField(choices=category_choices, required=False)
    imageURL = forms.URLField(label="URL for image", required=False)

class BidingForm(forms.Form):
    bid = forms.FloatField(label="")

class WatcllistForm(forms.Form):
    is_it_watchlist = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onchange': 'submit();'}))
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['item', 'purchaser']