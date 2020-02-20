# # -*- coding: utf-8 -*-
from django.urls import path
from .views import DummyAppSignupView

urlpatterns = [
    path('signup/<int:plugin_id>/', DummyAppSignupView.as_view(), name='signup'),
]
