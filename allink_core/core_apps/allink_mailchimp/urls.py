# -*- coding: utf-8 -*-
from django.urls import path

from allink_core.core_apps.allink_mailchimp.views import SignupView, SignupViewAdvanced


app_name = 'allink_mailchimp'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup_advanced/', SignupViewAdvanced.as_view(), name='signup_advanced'),
]
