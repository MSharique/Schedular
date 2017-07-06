from django.conf.urls import url, include
from django.contrib import admin
from .views import home, register, timezone, meeting, members, add_members

urlpatterns = [
    url(r'^$', home),
    url(r'^timezone/$', timezone),
    url(r'^register/$', register),
    url(r'^meeting/$', meeting),
    url(r'^members/$', members),
    url(r'^add_members/$', add_members, name='add_members'),
]