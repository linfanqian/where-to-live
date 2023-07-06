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

    platforms = forms.MultipleChoiceField(choices=PLATFORM_CHOICES)
    lowest_price = forms.IntegerField(required=False)
    highest_price = forms.IntegerField(required=False)
    location = forms.CharField(max_length=256, required=False)
    building_types = forms.MultipleChoiceField(choices=BUILDING_TYPE_CHOICES, required=False)
    include_water = forms.BooleanField(required=False)
    include_hydro = forms.BooleanField(required=False)
    include_internet = forms.BooleanField(required=False)
    independent_bathroom = forms.BooleanField(required=False)
    independent_kitchen = forms.BooleanField(required=False)


'''
class SubscribeForm(forms.Form):
    email = forms.EmailField()
    start_date = forms.DateField(
        widget=forms.NumberInput(attrs={'type': 'date'})
    )
    start_time = forms.DateTimeField()
    interval = forms.ChoiceField(
        choices=(
            (3, "3h"),
            (6, "6h"),
            (12, "12h"),
            (24, "24h"),
            (48, "48h"),
        )
    )
'''
