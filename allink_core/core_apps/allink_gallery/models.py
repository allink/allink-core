# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property

from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.folder import FilerFolderField
from djangocms_text_ckeditor.fields import HTMLField

from allink_core.core.utils import get_additional_templates


class AllinkGalleryPlugin(CMSPlugin):

    template = models.CharField(
        _('Template'),
        help_text=_('Choose a template.'),
        max_length=50
    )
    ratio = models.CharField(
        _('Ratio'),
        max_length=50,
        blank=True,
        null=True
    )
    fullscreen_enabled = models.BooleanField(
        _('Fullscreen option visible'),
        default=True,
        help_text=_('This option enables a fullscreen button for this gallery.'),
    )
    counter_enabled = models.BooleanField(
        _('Gallery counter visible'),
        default=False,
        help_text=_('This option enables a gallery counter.'),
    )
    auto_start_enabled = models.BooleanField(
        _('Autostart'),
        default=True,
        help_text=_('This option enables autoplay for this gallery.'),
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
    folder = FilerFolderField(
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text=_("All Images (.png, .gif, .jpg, .jpeg) will be used in gallery. "
                    "If a folder is specified, the child plugin won't be rendered."),
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

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        css_classes.append("counter-enabled") if self.counter_enabled else None
        return ' '.join(css_classes)

    @cached_property
    def folder_images(self):
        filename_extensions = ['png', 'gif', 'jpg', 'jpeg']
        images = []
        for image in self.folder.files:
            if image.extension in filename_extensions:
                images.append(image)
        return images

    def save(self, *args, **kwargs):
        super(AllinkGalleryPlugin, self).save(*args, **kwargs)
        AllinkGalleryImagePlugin.objects.filter(parent_id=self.id).update(template=self.template, ratio=self.ratio)


class AllinkGalleryImagePlugin(CMSPlugin):
    title = models.CharField(
        _('Title'),
        max_length=255,
        blank=True,
        null=True
    )
    text = HTMLField(
        _('Text'),
        blank=True,
        null=True
    )
    template = models.CharField(
        _('Template'),
        help_text=_('Choose a template.'),
        max_length=50,
    )
    ratio = models.CharField(
        _('Ratio'),
        max_length=50,
        blank=True,
        null=True
    )
    image = FilerImageField(
        verbose_name=_('Image'),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return'{}'.format(self.image)

    def save(self, *args, **kwargs):
        self.template = self.parent.allink_gallery_allinkgalleryplugin.template
        self.ratio = self.parent.allink_gallery_allinkgalleryplugin.ratio
        super(AllinkGalleryImagePlugin, self).save(*args, **kwargs)
