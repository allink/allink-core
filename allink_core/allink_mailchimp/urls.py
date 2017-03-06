# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import SignupView, SignupViewAdvanced

urlpatterns = patterns('',
    url(r'^singup/$', SignupView.as_view(), name="singup"),
    url(r'^singup_advanced/$', SignupViewAdvanced.as_view(), name="singup_advanced"),
)
