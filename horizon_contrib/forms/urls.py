
from django.conf.urls import patterns, url

from .views import CreateView, UpdateView

urlpatterns = patterns('',
    url(r'^models/(?P<cls_name>[\w\.\-]+)/create/$', CreateView.as_view(), name='create'),
    url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$', UpdateView.as_view(), name='update'),
)
