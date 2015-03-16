
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('horizon_contrib.generic.urls', namespace='generic')),
    url(r'^', include('horizon_contrib.forms.urls', namespace='forms')),
)
