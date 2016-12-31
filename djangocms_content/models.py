# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from cms.models.pluginmodel import CMSPlugin

from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from allink_core.allink_base.models import AllinkBasePlugin, AllinkBaseAppContentPlugin
from allink_core.allink_base.models.choices import HORIZONTAL_ALIGNMENT_CHOICES, CENTER

from settings import ALLOWED_VIDEO_EXTENSIONS


@python_2_unicode_compatible
class AllinkContentPlugin(AllinkBasePlugin):
    """
    A plugin representing different column-counts
    and special option for rendering its container-content compared to its Content-Plugins background-image.
    """

    COL_1 = 'col-1'
    COL_1_1 = 'col-1-1'
    COL_2_1 = 'col-2-1'
    COL_1_2 = 'col-1-2'
    COL_3 = 'col-3'

    COLUMN_AMOUNT = dict([
        (COL_1, 1),
        (COL_1_1, 2),
        (COL_2_1, 2),
        (COL_1_2, 2),
        (COL_3, 3),
    ])

    TEMPLATES = (
        (COL_1, '1 Column'),
        (COL_1_1, '2 Columns (1:1)'),
        (COL_2_1, '2 Columns (2:1)'),
        (COL_1_2, '2 Columns (1:2)'),
        (COL_3, '3 Columns'),
    )

    # General Fields
    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50,
        choices=TEMPLATES,
        default=TEMPLATES[0]
    )
    overlay_styles_enabled = models.BooleanField(
        _(u'Activate overlay styles'),
        help_text=_(u'If checked, the predefined overlay styles are applied (suitable when text is over an image/video)'),
        default=False
    )
    full_height_enabled = models.BooleanField(
        _(u'Activate "full height" mode'),
        help_text=_(u'If checked, the section will use the available height of the device\'s/browser\'s screen.'),
        default=False
    )
    bg_image_outer_container = FilerImageField(
        verbose_name=_(u'Background-Image'),
        help_text=_(u'Dimensions TBD'),
        related_name="content_bg_image",
        blank=True,
        null=True
    )
    parallax_enabled = models.BooleanField(
        _(u'Activate Parallax effect'),
        help_text=_(u'If checked, the parallax effect is enabled.'),
        default=False
    )
    bg_image_inner_container = FilerImageField(
        verbose_name=_(u'Background-Image'),
        help_text=_(u'Dimensions TBD'),
        related_name="content_container_bg_image",
        blank=True,
        null=True
    )

    # Video related fields
    video_file = FilerFileField(
        verbose_name=_(u'Source'),
        help_text=_(u'Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 4 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>Aspect ratio: TBD<br>File size: Dependent of video length. Generally speaking: Less is more.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='content_video_file'
    )
    video_poster_image = FilerImageField(
        verbose_name=_(u'Video Start Image'),
        related_name="content_video_poster_image",
        help_text=_(u'This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.'),
        blank=True,
        null=True
    )
    video_mobile_image = FilerImageField(
        verbose_name=_(u'Mobile Image'),
        related_name="content_video_moible_image",
        help_text=_(u'The image being displayed on mobile devices. Dimensions TBD'),
        blank=True,
        null=True
    )
    video_mobile_image_alignment = models.CharField(
        _(u'Mobile Image Alignment (horizontal)'),
        help_text=_(u'TBD Define which part of the image must be visible. Because we use the available space, there is a chance that a part (left and/or right) is not visible.'),
        max_length=50,
        choices=HORIZONTAL_ALIGNMENT_CHOICES,
        default=CENTER
    )

    def __str__(self):
        if self.title and self.template:
            return u'{} ({})'.format(self.title, self.template)
        elif self.template:
            return u'({})'.format(self.template)
        return str(self.pk)

    def clean(self):
            if (self.video_file and self.video_file.extension not in ALLOWED_VIDEO_EXTENSIONS):
                raise ValidationError(
                    _('Incorrect file type: %(value)s'),
                    params={'value': self.video_file.extension},
                )

    @property
    def css_classes(self):
        css_classes = self.base_classes

        css_classes.append('inner-container-has-bg-image') if self.bg_image_inner_container else None

        css_classes.append('parallax-enabled') if self.bg_image_outer_container and self.parallax_enabled else None
        css_classes.append("overlay-enabled") if self.overlay_styles_enabled else None

        css_classes.append("has-bg-video") if self.video_file and self.video_poster_image and self.video_mobile_image else None
        css_classes.append("full-height-enabled") if self.full_height_enabled else None
        css_classes.append("has-bg-image") if self.bg_image_outer_container else None
        css_classes.append("bg-image-outer-container-{}".format(self.id)) if self.bg_image_outer_container and not self.parallax_enabled else None
        css_classes.append(self.extra_css_classes)
        return ' '.join(css_classes)

    @property
    def section_has_content(self):
        # Property soll True zurueckgeben, wenn eine der folgenden Kritieren zutreffen..
        # - Ein Section Titel gesetzt ist..
        # - Mind. eine Column hat ein Kind
        return True


@python_2_unicode_compatible
class AllinkContentColumnPlugin(CMSPlugin):
    title = models.CharField(_(u'Title'), max_length=255, blank=True, null=True)

    def __str__(self):
        if self.title and self.template:
            return u'{} ({})'.format(self.title, self.template)
        else:
            return u'({})'.format(self.template)

    @property
    def template(self):
        return self.parent.djangocms_content_allinkcontentplugin.template
