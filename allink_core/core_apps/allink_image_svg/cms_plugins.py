from django.utils.translation import ugettext_lazy as _
from django import forms
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import AllinkImageSVGPlugin
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin
from allink_core.core.forms.fields import SelectLinkField


class AllinkImageSVGPluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):

    internal_link = SelectLinkField(label='Link Internal', required=False)

    class Meta:
        model = AllinkImageSVGPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkImageSVGPluginForm, self).__init__(*args, **kwargs)


@plugin_pool.register_plugin
class CMSAllinkImageSVGPlugin(CMSPluginBase):
    name = 'SVG Image'
    module = 'Generic'
    render_template = 'allink_image_svg/content.html'
    model = AllinkImageSVGPlugin
    form = AllinkImageSVGPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': [
                    'picture',
                    ('is_inline', 'is_fullwidth')
                ]
            }),
            ('Link settings', {
                'classes': ('collapse',),
                'fields': (
                    'internal_link',
                    'link_url',
                    ('link_mailto', 'link_phone'),
                    'link_anchor',
                    'link_file',
                    'link_target',
                )
            }),
        ]

        return fieldsets

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        return context
