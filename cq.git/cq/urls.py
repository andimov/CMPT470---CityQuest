from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cityquest/', include('cityquest.urls')),
    url(r'^login/', "django.contrib.auth.views.login", {'template_name': 'login.html'}),
    url(r'^logout/$', 'cq.views.logout'),
    url(r'^register/$', 'cq.views.register_user'),
    url(r'^register_success/$', 'cq.views.register_success'),
)

urlpatterns += staticfiles_urlpatterns()
