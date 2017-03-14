# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import AllinkInstagramPlugin


class AllinkInstagramPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkInstagramPlugin
        fields = (
            'template',
            'items_per_row',
            'paginated_by',
        )

    def __init__(self, *args, **kwargs):
        super(AllinkInstagramPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
