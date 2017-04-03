# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from allink_core.allink_mailchimp.views import SignupView, SignupViewAdvanced

urlpatterns = patterns(
    '',
    url(r'^singup/$', SignupView.as_view(), name="singup"),
    url(r'^singup_advanced/$', SignupViewAdvanced.as_view(), name="singup_advanced"),
)
