# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import DummyAppSignup


@admin.register(DummyAppSignup)
class DummyAppSignupAdmin(admin.ModelAdmin):
    pass
