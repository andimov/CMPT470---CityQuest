
from django.shortcuts import render_to_response, render, get_object_or_404 
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from cityquest.models import Event, UserProfile, Attendee, Comment
from cityquest.forms import EventForm, UserForm, EditEventForm, CommentForm
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from cityquest.admin import newUserChangeForm
from django.contrib.auth.forms import UserChangeForm


def event(request, event_id, slug):
#    event_cache_key = 'event_page' + str(event_id)
#    cache_time = 360 #TTL
#    result = cache.get(event_cache_key)
    event = Event.objects.get(id = event_id)
    attendees = Attendee.objects.filter(eventname = event)
    owner = get_user_model().objects.get(username = event.owner.username)
    comments = Comment.objects.filter(eventname = event)
    if request.user.is_authenticated():
        isAttending = Attendee.objects.filter(username = request.user).filter(eventname = event)
    else: 
        isAttending = 'none'
#    if not result:
    result = render_to_response('cityquest/event.html', {"event": event, "owner": owner, "attendees": attendees, "comments": comments, "isAttending": isAttending}, context_instance=RequestContext(request))
#        cache.set(event_cache_key, result, cache_time)
    return result

def home(request):
    result = render_to_response('cityquest/login.html', context_instance=RequestContext(request))
    return result

def eventlist(request):
    if request.method == 'GET':
        requestCategory = request.GET.get('category','')
	requestLocation = request.GET.get('location','')
        lat = request.GET.get('lat','')
        lon = request.GET.get('lon','')  
        filteredEvents = Event.objects.all().filter(category = requestCategory, public = True)
        events = {}
        distanceList = []
        for event in filteredEvents:
            distance = event.haversine(lon,lat)
            if distance < 30:
                events[distance] = event
                distanceList.append(distance)
	    distanceList.sort()
        result = render_to_response('cityquest/eventlist.html', {'events':events, 'distances': distanceList}, context_instance = RequestContext(request))
    else:
        events = Event.objects.all().filter(public = True)
    	result = render_to_response('cityquest/eventlist.html', {'events':events}, context_instance = RequestContext(request))
    return result

@login_required()
def myprofile(request):
    events = Event.objects.all()
    myevents = Attendee.objects.filter(username = request.user)
    result = render_to_response('cityquest/myprofile.html', {'events': events, "myevents": myevents}, context_instance=RequestContext(request))
    return result

@login_required()
def createevent(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = EditEventForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.owner = request.user
            instance.attendees = 1
            instance.slug = slugify(instance.eventname)
            instance.save()
            attendee = Attendee(username = request.user, eventname = instance)
            attendee.save()
            eventID = str(instance.id)
            linkRedirect = "/cq/cityquest/event/" + eventID + "/" + instance.slug
            return HttpResponseRedirect(linkRedirect)
        else:
            print form.errors
    else:
        form = EditEventForm()
    return render_to_response("cityquest/createEvent.html", {'form': form}, context)

@login_required()
def editevent(request, event_id, slug):
    context = RequestContext(request)
    currentEvent = Event.objects.get(id = event_id)
    if request.method == 'POST':
        form = EditEventForm(request.POST, instance = currentEvent)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.slug = slugify(instance.eventname)
            instance.save()
            return event(request, instance.id, instance.slug)
        else:
            print form.errors
    else:
        form = EditEventForm(instance = currentEvent)
#    cache.delete('event_page' + str(event_id))
    return render_to_response("cityquest/editEvent.html", {'form': form, 'event': currentEvent}, context)

@login_required()
def editprofile(request):
    context = RequestContext(request)
    me = get_user_model().objects.get(username = request.user.username)
    if request.method == 'POST':
        form = UserForm(request.POST, instance = me)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cq/cityquest/myprofile/')
        else:
            print form.errors
    else:
         form = UserForm(instance = me)
    return render_to_response("cityquest/editprofile.html", {'form': form}, context)

@login_required()
def attend(request, event_id):
    currentEvent = get_object_or_404(Event, id = event_id)
    if request.method == 'POST':
        currentEvent.attendees += 1
        currentEvent.save()
        attendee = Attendee(username = request.user, eventname = currentEvent)
        attendee.save()
    eventID = str(event_id)
    linkRedirect = "/cq/cityquest/event/" + eventID + "/" + currentEvent.slug
#    cache.delete('event_page' + str(event_id))
    return HttpResponseRedirect(linkRedirect)

@login_required()
def unattend(request, event_id):
    currentEvent = get_object_or_404(Event, id = event_id)
    if request.method == 'POST':
        currentEvent.attendees -= 1
        currentEvent.save()
        attendee = Attendee.objects.filter(username = request.user).filter(eventname = currentEvent)
        attendee.delete()
    eventID = str(event_id)
    linkRedirect = "/cq/cityquest/event/" + eventID + "/" + currentEvent.slug
#    cache.delete('event_page' + str(event_id))
    return HttpResponseRedirect(linkRedirect)


@login_required()
def commentevent(request, event_id):
    context = RequestContext(request)
    currentEvent = Event.objects.get(id = event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.username = request.user
            instance.eventname = currentEvent
            instance.save()
            eventID = str(currentEvent.id)
            linkRedirect = "/cq/cityquest/event/" + eventID + "/" + currentEvent.slug
            return HttpResponseRedirect(linkRedirect)
        else:
            print form.errors
    else:
        form = CommentForm()
#    cache.delete('event_page' + str(event_id))
    return render_to_response("cityquest/comment.html", {'form': form, 'event': currentEvent}, context)

