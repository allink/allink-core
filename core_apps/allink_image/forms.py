# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.core.utils import get_ratio_choices_orig, get_additional_choices, get_project_color_choices
from allink_core.core_apps.allink_image.models import AllinkImagePlugin
from allink_core.core.forms.fields import ColorField
from allink_core.core.forms.fields import SelectLinkField
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin


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
            help_text=_(u'Important: In case the selected option is a <strong>form</strong>, make sure the select the <strong>Lightbox (Forms)</strong> from the <strong>link target</strong> options for best user experience.'),
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

        if get_additional_choices('IMAGE_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations'),
                choices=get_additional_choices('IMAGE_CSS_CLASSES'),
                required=False,
            )
