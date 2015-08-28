
from django.conf.urls import patterns, url
from horizon_contrib.forms.views import CreateView, UpdateView

from .views import GenericIndexView, DataView

urlpatterns = patterns('',
    url(r'^models/(?P<cls_name>[\w\.\-]+)/create/$', CreateView.as_view(), name='create'),
    url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$', UpdateView.as_view(), name='update'),
    # tables
    url(r'^models/(?P<cls_name>[\w\.\-]+)/index/$', GenericIndexView.as_view(), name='index'),
    url(r'^models/(?P<cls_name>[\w\.\-]+)/index/json$', DataView.as_view(), name='data'),
    url(r'^models/(?P<cls_name>[\w\.\-]+)/index/(?P<table>[\w\.\-]+)/$', GenericIndexView.as_view(), name='index'),
    url(r'^models/(?P<cls_name>[\w\.\-]+)/index/(?P<table>[\w\.\-]+)/json$', DataView.as_view(), name='data'),
)
