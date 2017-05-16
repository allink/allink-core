# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.allink_legacy_redirect.models import AllinkLegacyLink
from allink_core.allink_base.forms.fields import SelectLinkField
from allink_core.allink_base.forms.mixins import AllinkInternalLinkFieldMixin


class AllinkLegacyChangeAdminForm(AllinkInternalLinkFieldMixin, forms.ModelForm):
    new_link = SelectLinkField(label=_('New Page'))

    class Meta:
        model = AllinkLegacyLink
        fields = ['old', 'overwrite', 'active', 'match_subpages']
