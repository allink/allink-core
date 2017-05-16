# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField

from allink_core.allink_base.utils import get_additional_templates



@python_2_unicode_compatible
class AllinkGalleryPlugin(CMSPlugin):

    SLIDER = 'slider'

    TEMPLATES = (
        (SLIDER, 'Slider'),
    )
    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50,
        default=TEMPLATES[0]
    )
    ratio = models.CharField(
        _(u'Ratio'),
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        if self.template:
            return self.template
        return str(self.pk)

    @classmethod
    def get_templates(cls):
        templates = cls.TEMPLATES
        for x, y in get_additional_templates('Gallery'):
            templates += ((x, y),)
        return templates


@python_2_unicode_compatible
class AllinkGalleryImagePlugin(CMSPlugin):
    title = models.CharField(
        _(u'Title'),
        max_length=255,
        blank=True,
        null=True
    )
    text = HTMLField(
        _(u'Text'),
        blank=True,
        null=True
    )
    image = FilerImageField(verbose_name=_(u'Image'))

    def __str__(self):
        return u'{}'.format(self.image)

    @property
    def template(self):
        return self.parent.djangocms_gallery_allinkgalleryplugin.template
