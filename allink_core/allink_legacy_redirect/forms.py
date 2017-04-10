# -*- coding: utf-8 -*-
from django import forms

from allink_core.allink_legacy_redirect.models import AllinkLegacyLink
from allink_core.allink_base.models.model_fields import choices_from_sitemaps


class AllinkLegacyChangeAdminForm(forms.ModelForm):
    new_page = forms.ChoiceField(choices=())

    class Meta:
        model = AllinkLegacyLink
        fields = ['old', 'new_page', 'overwrite', 'active', 'match_subpages']

    def __init__(self, *args, **kwargs):
        super(AllinkLegacyChangeAdminForm, self).__init__(*args, **kwargs)
        self.fields['new_page'].choices = choices_from_sitemaps()
