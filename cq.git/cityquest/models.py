from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from time import time
from math import radians, cos, sin, asin, sqrt

class Event(models.Model):
    eventname = models.CharField(max_length = 100, null = False)
    address = models.CharField(max_length = 200, null = False)
    CATEGORIES = (
        (u'Business', u'Business'),
        (u'Charity', u'Charity'),
        (u'ClassesWorkshops', u'Classes & Workshops'),
        (u'Conferences', u'Conferences'),
        (u'Festivals', u'Festivals'),
        (u'FoodDrinks', u'Food & Drinks'),
        (u'MusicConcerts', u'Music & Concerts'),
        (u'Networking', u'Networking'),
        (u'Nightlife', u'Nightlife'),
        (u'PerformingArts', u'Performing Arts'),
        (u'ScienceTech', u'Science & Tech'),
        (u'Spirituality', u'Spirituality'),
        (u'Sports', u'Sports'),
        (u'Other', u'Other')
    )
    category = models.CharField(max_length = 30, choices = CATEGORIES, null = False)
    price = models.DecimalField(null = False, max_digits = 7, decimal_places = 2)
    datetime = models.DateTimeField(null = False)
    description = models.TextField(null = True, blank = True)
    public = models.BooleanField()
    owner = models.ForeignKey('UserProfile', blank = True, null = True)
    attendees = models.IntegerField(blank = True, null = True, default = 1)
    slug = models.SlugField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)
    latitude = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.eventname

    def haversine(self, lon, lat):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
	# convert lon and lat to floats first
	lon = float(lon)
	lat = float(lat)
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon, lat, self.longitude, self.latitude])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 

        # 6367 km is the radius of the Earth
        km = 6367 * c
        return km

class Attendee(models.Model):
    username = models.ForeignKey('UserProfile')
    eventname = models.ForeignKey('Event')

class Comment(models.Model):
    username = models.ForeignKey('UserProfile')
    eventname = models.ForeignKey('Event')
    commentbody = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.commentbody


class UserProfile(AbstractUser):
    about_me = models.TextField(null = True, blank = True)
    ph_number = models.CharField(max_length = 15, null = True, blank = True)
    age = models.IntegerField(null = True, blank = True)
    SEX_CHOICES = (
        (u'1', u'Female'),
        (u'2', u'Male'),
    )
    sex = models.CharField(max_length = 1, choices = SEX_CHOICES)
    location = models.CharField(max_length = 100, null = True, blank = True)

    def __str__(self):
        return self.ph_number


