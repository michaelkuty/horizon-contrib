
from django.conf.urls import patterns, include, url

urlpatterns = patterns('horizon_contrib',
    url(r'^', include('horizon_contrib.generic.urls', namespace='generic')),
)
