# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from allink_core.core.utils import get_additional_choices
from allink_core.core_apps.allink_social_icon.models import AllinkSocialIconContainerPlugin, AllinkSocialIconPlugin


class AllinkSocialIconContainerPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkSocialIconContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
    
    def __init__(self, *args, **kwargs):
        super(AllinkSocialIconContainerPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('SOCIAL_ICON_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations for Social Icon Plugin'),
                choices=get_additional_choices('SOCIAL_ICON_CSS_CLASSES'),
                required=False,
            )


class AllinkSocialIconPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkSocialIconPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
    
    def __init__(self, *args, **kwargs):
        super(AllinkSocialIconPluginForm, self).__init__(*args, **kwargs)
        
        if get_additional_choices('SOCIAL_ICONS_CHOICES'):
            self.fields['icon'] = forms.ChoiceField(
                widget=forms.Select(),
                label=_(u'Icon choices for Social Icon Plugin'),
                choices=get_additional_choices('SOCIAL_ICONS_CHOICES'),
                required=True,
            )


@plugin_pool.register_plugin
class CMSAllinkSocialIconContainerPlugin(CMSPluginBase):
    model = AllinkSocialIconContainerPlugin
    name = _('Social Icon Container')
    module = _('Generic')
    allow_children = True
    child_classes = ['CMSAllinkSocialIconPlugin']
    form = AllinkSocialIconContainerPluginForm
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = ()
        if get_additional_choices('SOCIAL_ICON_CSS_CLASSES'):
            fieldsets = (
                (None, {
                    'fields': (
                        'project_css_classes',
                    ),
                }),
            )

        return fieldsets


    def get_render_template(self, context, instance, placeholder):
        template = 'allink_social_icon/content.html'
        return template


@plugin_pool.register_plugin
class CMSAllinkSocialIconPlugin(CMSPluginBase):
    model = AllinkSocialIconPlugin
    name = _('Social Icon')
    module = _('Generic')
    allow_children = False
    form = AllinkSocialIconPluginForm
    text_enabled = False

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'icon',
                    'link',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_social_icon/item.html'
        return template
