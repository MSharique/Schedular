from django.conf.urls import url, include
from django.contrib import admin
from .views import home, register, timezone, meeting, members, add_members, feedback

urlpatterns = [
    url(r'^$', home),
    url(r'^timezone/$', timezone),
    url(r'^register/$', register),
    url(r'^meeting/$', meeting),
    url(r'^members/$', members),
    url(r'^add_members/$', add_members, name='add_members'),
    url(r'^feedback/$', feedback, name='feedback'),
	url(r'^feedback/(?P<hm>[\w]+)/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<status>[\d])$', feedback, name='feedback'),
]