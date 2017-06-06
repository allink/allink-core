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

    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50
    )
    ratio = models.CharField(
        _(u'Ratio'),
        max_length=50,
        blank=True,
        null=True
    )
    fullscreen_enabled = models.BooleanField(
        _(u'Fullscreen option visible'),
        default=False,
        help_text=_(u'This option enables a fullscreen button for this gallery.'),
    )
    counter_enabled = models.BooleanField(
        _(u'Gallery counter visible'),
        default=False,
        help_text=_(u'This option enables a gallery counter.'),
    )
    auto_start_enabled = models.BooleanField(
        _(u'Autostart'),
        default=True,
        help_text=_(u'This option enables autoplay for this gallery.'),
    )

    def __str__(self):
        if self.template:
            return self.template
        return str(self.pk)

    @classmethod
    def get_templates(cls):
        templates = ()
        for x, y in get_additional_templates('GALLERY'):
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
