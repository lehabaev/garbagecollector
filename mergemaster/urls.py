#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'message/$', 'mergemaster.views.AjaxMergeNotification'),
  url(r'^$', 'mergemaster.views.MergeList'),
  url(r'^discus/(?P<pid>(\d+))/$', 'mergemaster.views.MergeDiscus'),
  url(r'^discus/load/(?P<pid>(\d+))/$', 'mergemaster.views.MergeDiscusLoad'),
  url(r'^(?P<action>(\w+))/(?P<pid>(\d+))/$', 'mergemaster.views.MergeAction'),
  url(r'api/$', 'mergemaster.views.ApiAddRequest'),

  )