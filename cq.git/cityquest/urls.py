from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url
from cityquest import views

urlpatterns = patterns('',
    url(r'^home/', views.home),
    url(r'^event/(?P<event_id>\d+)/(?P<slug>[-\w]+)/', views.event),
    url(r'^eventlist/', views.eventlist),
    url(r'^create/', views.createevent),
    url(r'^edit/(?P<event_id>\d+)/(?P<slug>[-\w]+)/', views.editevent),
    url(r'^attend/(?P<event_id>\d+)/', views.attend),
    url(r'^unattend/(?P<event_id>\d+)/', views.unattend),
    url(r'^comment/(?P<event_id>\d+)/', views.commentevent),
    url(r'^myprofile/', views.myprofile),
    url(r'^editprofile/', views.editprofile),
)
