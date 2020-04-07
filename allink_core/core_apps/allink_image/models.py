# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext
from django.contrib.postgres.fields import ArrayField

from djangocms_attributes_field.fields import AttributesField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from allink_core.core.models import AllinkLinkFieldsModel
from allink_core.core.models.fields import CMSPluginField


class AllinkImagePlugin(AllinkLinkFieldsModel, CMSPlugin):
    """
     Renders an image with the option of adding a link
    """

    picture = FilerImageField(
        verbose_name='Image',
        null=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_picture',
    )
    ratio = models.CharField(
        'Ratio',
        max_length=50,
        blank=True,
        null=True
    )
    bg_enabled = models.BooleanField(
        verbose_name='Placeholder Background Color',
        blank=True,
        default=True,
        help_text=('Show default image placeholder background color.<br><strong>Important:</strong> '
                   'Disabling this option results in a transparent background even if a specific color is set '
                   '(this makes sense when a transparent PNG image is used)'),
    )
    icon_enabled = models.BooleanField(
        verbose_name='Loader Icon',
        blank=True,
        default=False,
        help_text=('Show the icon that is used as long as the image is loading.<br>'
                   '<strong>Important:</strong> Disable this option if a transparent PNG image is used.'),
    )
    bg_color = models.CharField(
        'Set a predefined background color',
        max_length=50,
        blank=True,
        null=True
    )
    caption_text = models.TextField(
        verbose_name='Caption text',
        blank=True,
        help_text='Provide a description, attribution, copyright or other information.'
    )
    attributes = AttributesField(
        verbose_name='Attributes',
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
        'Width Alias',
        max_length=50,
        blank=True,
        null=True
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        if self.picture and self.picture.label:
            return self.picture.label
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(AllinkImagePlugin, self).save(*args, **kwargs)

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
