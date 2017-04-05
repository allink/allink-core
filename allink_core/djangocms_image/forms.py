# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.djangocms_image.models import AllinkImagePlugin
from allink_core.allink_base.models.model_fields import choices_from_sitemaps


class AllinkImagePluginForm(forms.ModelForm):

    link_internal = forms.ChoiceField(choices=(), required=False)

    class Meta:
        model = AllinkImagePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
        widgets = {
            'caption_text': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(AllinkImagePluginForm, self).__init__(*args, **kwargs)
        self.fields['link_special'] = forms.CharField(
            label=_(u'Special Links'),
            widget=forms.Select(choices=self.instance.get_link_special_choices()),
            required=False,
        )
        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default settings for the content plugin.'),
            widget=forms.Select(choices=self.instance.get_ratio_choices()),
            required=False,
        )
        self.fields['link_internal'].choices = choices_from_sitemaps()
