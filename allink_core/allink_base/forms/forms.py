# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from parler.forms import TranslatableModelForm


class AllinkBaseModelForm(forms.ModelForm):
    pass

class AllinkBaseTranslatableModelForm(TranslatableModelForm):
    pass
