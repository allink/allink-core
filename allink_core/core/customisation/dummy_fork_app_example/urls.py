# -*- coding: utf-8 -*-
"""
use core:
no 'urls.py' file needed

!important!
- make sure you also add the new urls to the cms_apps.py so djangocms knows about them! override the apphook,
see example in cms_apps.py
- make sure you respect the patterns in 'allink_core.apps.dummy_app.urls'
"""
from django.urls import path
from .views import DummyAppSomeNewView

urlpatterns = [
    path('new/some-new-view/', DummyAppSomeNewView.as_view(), name='some-new-view'),
]
