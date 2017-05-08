# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.postgres.fields import ArrayField

from djangocms_attributes_field.fields import AttributesField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField

from allink_core.allink_base.utils import get_additional_templates
from allink_core.allink_base.utils.utils import get_project_color_choices
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

    project_css_classes = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True
        ),
        blank=True,
        null=True
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

    @property
    def base_classes(self):
        css_classes = []
        css_classes.append("has-bg-color") if self.bg_color else None
        css_classes.append(get_project_color_choices()[self.bg_color]) if self.bg_color else None
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return css_classes

    @property
    def css_classes(self):
        css_classes = self.base_classes
        return ' '.join(css_classes)

    def get_short_description(self):
        if self.external_picture:
            return self.external_picture
        if self.picture and self.picture.label:
            return self.picture.label
        return ugettext('<file is missing>')

    def copy_relations(self, oldinstance):
        self.picture = oldinstance.picture
