# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import python_2_unicode_compatible
from djangocms_attributes_field.fields import AttributesField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from allink_core.allink_base.models.choices import BLANK_CHOICE, RATIO_CHOICES
from allink_core.allink_base.utils import get_additional_templates, get_additional_choices
from allink_core.allink_base.models.reusable_fields import AllinkLinkFieldsModel
from allink_core.allink_base.models.model_fields import CMSPluginField


@python_2_unicode_compatible
class AllinkImagePlugin(AllinkLinkFieldsModel, CMSPlugin):
    """
     Renders an image with the option of adding a link
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
    picture = FilerImageField(
        verbose_name=_(u'Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_picture',
    )
    external_picture = models.URLField(
        verbose_name=_(u'External image'),
        blank=True,
        max_length=255,
        help_text=_(u'If provided, overrides the embedded image. '
                    u'Certain options such as cropping are not applicable to external images.')
    )
    ratio = models.CharField(
        _(u'Ratio'),
        max_length=50,
        choices=RATIO_CHOICES,
        blank=True,
        null=True
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
    # section wireframe
    width = models.PositiveIntegerField(
        verbose_name=_(u'Width'),
        blank=True,
        null=True,
        help_text=_(u'The image width as number in pixels. '
                    u'Example: "720" and not "720px".'),
    )
    use_no_cropping = models.BooleanField(
        verbose_name=_(u'Use original image'),
        blank=True,
        default=False,
        help_text=_(u'Outputs the raw image without cropping.'),
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        if self.picture and self.picture.label:
            return self.picture.label
        return str(self.pk)

    @classmethod
    def get_templates(cls):
        templates = cls.TEMPLATES
        for x, y in get_additional_templates('AllinkImagePlugin'):
            templates += ((x, y),)
        return templates

    @classmethod
    def get_ratio_choices(cls):
        return BLANK_CHOICE + RATIO_CHOICES + get_additional_choices('RATIO_CHOICES')

    def get_short_description(self):
        if self.external_picture:
            return self.external_picture
        if self.picture and self.picture.label:
            return self.picture.label
        return ugettext('<file is missing>')

    def copy_relations(self, oldinstance):
        self.picture = oldinstance.picture
