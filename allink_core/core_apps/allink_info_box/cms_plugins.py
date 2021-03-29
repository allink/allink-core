# -*- coding: utf-8 -*-
from django import forms
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from allink_core.core_apps.allink_info_box.models import AllinkInfoBoxPlugin


class AllinkInfoBoxPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkInfoBoxPlugin
        fields = (
            'template',
            'counter',
            'transparent_background'
        )

    def __init__(self, *args, **kwargs):
        super(AllinkInfoBoxPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label='Template',
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )


@plugin_pool.register_plugin
class CMSAllinkInfoBoxPlugin(CMSPluginBase):
    model = AllinkInfoBoxPlugin
    name = 'Info Box'
    module = 'Generic'
    cache = False
    allow_children = True
    child_classes = ['TextPlugin', 'CMSAllinkImagePlugin']
    form = AllinkInfoBoxPluginForm

    def get_render_template(self, context, instance, placeholder, file='content'):
        template = 'allink_info_box/plugins/{}/{}.html'.format(instance.template, file)
        return template
