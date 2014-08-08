from django import forms
from cityquest.models import Event, UserProfile, Comment
from django.forms import ModelForm
from cityquest.admin import newUserChangeForm
from django.contrib.auth import get_user_model

class EventForm(ModelForm):
    class Meta:
        model = Event

class UserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('about_me','ph_number', 'age', 'sex', 'location')

class EditEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('eventname', 'address', 'category', 'datetime', 'price', 'description', 'public', 'latitude', 'longitude')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('commentbody',)
