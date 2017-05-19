# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.allink_base.utils import get_ratio_choices_orig, get_additional_choices, get_project_color_choices
from allink_core.djangocms_image.models import AllinkImagePlugin
from allink_core.allink_base.forms.fields import ColorField
from allink_core.allink_base.forms.fields import SelectLinkField
from allink_core.allink_base.forms.mixins import AllinkInternalLinkFieldMixin


class AllinkImagePluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):

    internal_link = SelectLinkField(label=_('Link Internal'), required=False)

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
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default image ratio set for images in a colum of a content section.'),
            widget=forms.Select(choices=get_ratio_choices_orig()),
            required=False,
        )
        if get_project_color_choices():
            self.fields['bg_color'] = ColorField(
                label=_(u'Set a predefined background color'),
                required=False,
            )
        if get_additional_choices('IMAGE_PLUGIN_PROJECT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined css classes'),
                help_text=_(u'Instructions: Single selection is made by clicking on an option. Multiple selections are achieved by pressing and holding down the Command-key (Mac) or Control-Key (Windows) <strong>and</strong> clicking the options you would like to apply.'),
                choices=get_additional_choices('IMAGE_PLUGIN_PROJECT_CSS_CLASSES'),
                required=False,
            )
