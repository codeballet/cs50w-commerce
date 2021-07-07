from django import forms

from .models import Category


class BidForm(forms.Form):
    bid = forms.DecimalField(label='New bid', max_digits=8, decimal_places=2)


class ListingForm(forms.Form):
    categories = []
    for category in Category.objects.all():
        categories.append((str(category), str(category).capitalize()))

    title = forms.CharField(label='Title', max_length=250, required=True)
    description = forms.CharField(label='Description', max_length=500, widget=forms.Textarea, required=True)
    start_bid = forms.DecimalField(max_digits=8, decimal_places=2, required=True)
    image_url = forms.URLField(label='Image URL', max_length=200, required=False)
    categories = forms.MultipleChoiceField(
        label="Categories",
        widget=forms.CheckboxSelectMultiple, 
        choices=categories,
        required=False
    )
