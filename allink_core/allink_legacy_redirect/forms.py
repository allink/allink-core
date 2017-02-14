# -*- coding: utf-8 -*-
from django import forms

from .models import AllinkLegacyLink

class AllinkLegacyChangeAdminForm(forms.ModelForm):

    class Meta:
        model = AllinkLegacyLink
        fields = ['old', 'new', 'overwrite', 'active', 'match_subpages']
