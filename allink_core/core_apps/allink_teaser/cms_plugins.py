# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from cms.models.pagemodel import Page
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from allink_core.core.models.mixins import AllinkTeaserMixin
from allink_core.apps.config.utils import get_page_teaser_dict
from allink_core.core.forms.fields import SelectLinkField
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin
from allink_core.core_apps.allink_teaser.models import AllinkTeaserPlugin


class AllinkTeaserPluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):

    internal_link = SelectLinkField(label=_('Link Internal'))

    class Meta:
        model = AllinkTeaserPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkTeaserPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label=_('Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )


@plugin_pool.register_plugin
class CMSAllinkTeaserPlugin(CMSPluginBase):
    model = AllinkTeaserPlugin
    name = _('Teaser')
    module = _('Generic')
    form = AllinkTeaserPluginForm

    class Media:
        js = (
            get_files('djangocms_custom_admin')[1]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[0]['publicPath'],

            )
        }

    fieldsets = (
        (None, {
            'fields': (
                'template',
                'internal_link',
            ),
        }),
        ('Override teaser content', {
            'classes': ('collapse',),
            'fields': (
                'teaser_image',
                'teaser_title',
                'teaser_technical_title',
                'teaser_description',
                'teaser_link_text',
            )
        })
    )

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_teaser/{}/item.html'.format(instance.template)
        return template

    def render(self, context, instance, placeholder):
        context = super(CMSAllinkTeaserPlugin, self).render(context, instance, placeholder)
        context.update(self.get_teaser_context(instance))
        return context

    def get_teaser_override_fields(self, instance, teaser_dict):
        for field in filter(lambda x: x.name.startswith('teaser_'), instance._meta.get_fields()):
            if getattr(instance, field.name):
                teaser_dict[field.name] = getattr(instance, field.name)

    def get_teaser_context(self, instance):
        teaser_dict = dict()

        # check if link object is a page
        if issubclass(instance.link_object.__class__, Page):
            teaser_dict = get_page_teaser_dict(instance.link_object)
        # check if link object is a app detail link
        elif issubclass(instance.link_object.__class__, AllinkTeaserMixin):
            teaser_dict = instance.link_object.teaser_dict

        # override fields from teaser plugin
        self.get_teaser_override_fields(instance, teaser_dict)

        return teaser_dict
