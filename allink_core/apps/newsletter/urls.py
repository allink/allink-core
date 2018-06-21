# -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.apps.newsletter.views import SignupView

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
]
