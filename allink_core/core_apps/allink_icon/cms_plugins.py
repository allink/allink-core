# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.core.utils import get_additional_choices
from allink_core.core_apps.allink_icon.models import AllinkIconPlugin


class AllinkIconPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkIconPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
    
    def __init__(self, *args, **kwargs):
        super(AllinkIconPluginForm, self).__init__(*args, **kwargs)
        
        if get_additional_choices('ICONS_CHOICES'):
            self.fields['icon'] = forms.ChoiceField(
                widget=forms.Select(),
                label=_(u'Icon choices for Social Icon Plugin'),
                choices=get_additional_choices('ICONS_CHOICES'),
                required=True,
            )
        if get_additional_choices('ICON_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations for Social Icon Plugin'),
                choices=get_additional_choices('ICON_CSS_CLASSES'),
                required=False,
            )


@plugin_pool.register_plugin
class CMSAllinkIconPlugin(CMSPluginBase):
    model = AllinkIconPlugin
    name = _('Icon')
    module = _('Generic')
    allow_children = False
    form = AllinkIconPluginForm
    text_enabled = False

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'icon',
                ),
            }),
        )

        if get_additional_choices('ICON_CSS_CLASSES'):
            fieldsets +=  (
                (None, {
                    'fields': (
                        'project_css_classes',
                    ),
                }),
            )
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_icon/content.html'
        return template
