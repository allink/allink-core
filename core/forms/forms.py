# -*- coding: utf-8 -*-
from django import forms
from parler.forms import TranslatableModelForm


class AllinkBaseModelForm(forms.ModelForm):
    pass


class AllinkBaseTranslatableModelForm(TranslatableModelForm):
    pass
