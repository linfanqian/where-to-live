from django import forms

from .models import SearchCondition

from .enums import Platform

class SearchForm(forms.Form):
    PLATFORM_CHOICES = [
        (Platform.HOUSE51, "house.51.ca"),
        (Platform.YORKBBS, "yorkbbs.ca"),
    ]
    BUILDING_TYPE_CHOICES = [
        ("CONDO", "Condo"),
        ("TOWNHOUSE", "Townhouse"),
        ("SEMI-DETACHED", "Semi-Detached"),
        ("DETACHED", "Detached"),
    ]

    platforms = forms.MultipleChoiceField(
        choices=PLATFORM_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    lowest_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    highest_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=256, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    building_types = forms.MultipleChoiceField(
        choices=BUILDING_TYPE_CHOICES, 
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    include_water = forms.BooleanField(required=False)
    include_hydro = forms.BooleanField(required=False)
    include_internet = forms.BooleanField(required=False)
    independent_bathroom = forms.BooleanField(required=False)
    independent_kitchen = forms.BooleanField(required=False)

class SubscribeForm(forms.Form):
    EMAIL_INTERVAL = [
        (6, "6h"),
        (12, "12h"),
        (24, "24h"),
        (48, "48h"),
    ]

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(
        widget=forms.NumberInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        widget=forms.NumberInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    interval = forms.ChoiceField(
        choices=EMAIL_INTERVAL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
