# -*- coding: utf-8 -*-
from django.urls import path

from allink_core.apps.newsletter.views import SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
]
