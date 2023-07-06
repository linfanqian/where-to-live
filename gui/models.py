import sys

from django.db import models

class SearchCondition(models.Model):
    platforms = models.CharField(max_length=256)
    lowest_price = models.IntegerField(default=0)
    highest_price = models.IntegerField(default=sys.maxsize)
    location = models.CharField(max_length=256, blank=True, null=True)
    building_types = models.CharField(max_length=256, blank=True, null=True)
    include_water = models.BooleanField(default=False)
    include_hydro = models.BooleanField(default=False)
    include_internet = models.BooleanField(default=False)
    independent_bathroom = models.BooleanField(default=False)
    independent_kitchen = models.BooleanField(default=False)

class Notice(models.Model):
    email = models.EmailField(primary_key=True, max_length=256)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    interval = models.IntegerField()  # unit in hour
