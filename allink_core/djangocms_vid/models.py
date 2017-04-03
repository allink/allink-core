# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from djangocms_attributes_field.fields import AttributesField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from allink_core.allink_base.models.choices import BLANK_CHOICE, RATIO_CHOICES
from allink_core.allink_base.utils import get_additional_templates, get_additional_choices
from allink_core.allink_base.models.model_fields import CMSPluginField


@python_2_unicode_compatible
class AllinkVidPlugin(CMSPlugin):
    """
    Renders either an Iframe when ``link`` is provided or the HTML5 <video> tag
    """

    # TEMPLATES
    DEFAULT = 'default'

    TEMPLATES = (
        (DEFAULT, 'Default'),
    )

    # FIELDS
    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50,
        choices=TEMPLATES,
        default=TEMPLATES[0]
    )

    label = models.CharField(
        verbose_name=_('Label'),
        blank=True,
        max_length=255,
    )
    embed_link = models.CharField(
        verbose_name=_('Embed link'),
        blank=True,
        max_length=255,
        help_text=_(u'Use this field to embed videos from external services such as YouTube, Vimeo or others. Leave it blank to upload video files by adding nested "Source" plugins.'),
    )
    poster = FilerImageField(
        verbose_name=_('Poster'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    attributes = AttributesField(
        verbose_name=_(u'Attributes'),
        blank=True,
    )
    ratio = models.CharField(
        _(u'Ratio'),
        max_length=50,
        choices=RATIO_CHOICES,
        blank=True,
        null=True
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return self.label or self.embed_link or str(self.pk)

    def copy_relations(self, oldinstance):
        self.poster = oldinstance.poster

    @classmethod
    def get_templates(cls):
        templates = cls.TEMPLATES
        for x, y in get_additional_templates('AllinkVidPlugin'):
            templates += ((x, y),)
        return templates

    @classmethod
    def get_ratio_choices(cls):
        return BLANK_CHOICE + RATIO_CHOICES + get_additional_choices('RATIO_CHOICES')
