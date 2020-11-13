# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import DummyAppSignup


class DummyAppSignupForm(ModelForm):
    class Meta:
        model = DummyAppSignup
        fields = '__all__'