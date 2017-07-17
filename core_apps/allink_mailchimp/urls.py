# -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.core_apps.allink_mailchimp.views import SignupView, SignupViewAdvanced

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^signup_advanced/$', SignupViewAdvanced.as_view(), name='signup_advanced'),
]
