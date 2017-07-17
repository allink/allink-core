# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.core.loading import get_model

Work = get_model('work', 'Work')


class WorkSearchForm(forms.Form):
    q = forms.CharField(label=_(u'Product Search'), required=False)
