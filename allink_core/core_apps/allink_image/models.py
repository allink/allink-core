# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.postgres.fields import ArrayField

from djangocms_attributes_field.fields import AttributesField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from allink_core.core.models.models import AllinkLinkFieldsModel
from allink_core.core.models.fields import CMSPluginField


@python_2_unicode_compatible
class AllinkImagePlugin(AllinkLinkFieldsModel, CMSPlugin):
    """
     Renders an image with the option of adding a link
    """

    picture = FilerImageField(
        verbose_name=_(u'Image'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_picture',
    )
    ratio = models.CharField(
        _(u'Ratio'),
        max_length=50,
        blank=True,
        null=True
    )
    bg_enabled = models.BooleanField(
        verbose_name=_(u'Placeholder Background Color'),
        blank=True,
        default=True,
        help_text=_(u'Show default image placeholder background color.<br><strong>Important:</strong> Disabling this option results in a transparent background even if a specific color is set (this makes sense when a transparent PNG image is used)'),
    )
    icon_enabled = models.BooleanField(
        verbose_name=_(u'Loader Icon'),
        blank=True,
        default=True,
        help_text=_(u'Show the icon that is used as long as the image is loading.<br><strong>Important:</strong> Disable this option if a transparent PNG image is used.'),
    )
    bg_color = models.CharField(
        _(u'Set a predefined background color'),
        max_length=50,
        blank=True,
        null=True
    )
    caption_text = models.TextField(
        verbose_name=_(u'Caption text'),
        blank=True,
        help_text=_(u'Provide a description, attribution, copyright or other information.')
    )
    attributes = AttributesField(
        verbose_name=_(u'Attributes'),
        blank=True,
        excluded_keys=['src', 'width', 'height'],
    )
    project_css_classes = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True
        ),
        blank=True,
        null=True
    )
    width_alias = models.CharField(
        _(u'Width Alias'),
        max_length=50,
        blank=True,
        null=True
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        if self.picture and self.picture.label:
            return self.picture.label
        return str(self.pk)

    @property
    def css_classes(self):
        css_classes = []
        css_classes.append("has-bg-color") if self.bg_color else None
        css_classes.append(self.bg_color) if self.bg_color else None
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return ' '.join(css_classes)

    def get_short_description(self):
        if self.picture and self.picture.label:
            return self.picture.label
        return ugettext('<file is missing>')

    def copy_relations(self, oldinstance):
        self.picture = oldinstance.picture

    def save(self, *args, **kwargs):
        super(AllinkImagePlugin, self).save(*args, **kwargs)
