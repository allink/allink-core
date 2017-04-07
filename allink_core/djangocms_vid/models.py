# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from djangocms_attributes_field.fields import AttributesField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from allink_core.allink_base.utils import get_additional_choices
from allink_core.allink_base.models.choices import VIDEO_SERVICE_CHOICES, BLANK_CHOICE, RATIO_CHOICES
from allink_core.allink_base.models.model_fields import CMSPluginField



@python_2_unicode_compatible
class AllinkVidBasePlugin(CMSPlugin):

    class Meta:
        abstract = True

    auto_start_enabled = models.BooleanField(
        _(u'Autostart'),
        default=True
    )
    allow_fullscreen_enabled = models.BooleanField(
        _(u'Allow fullscreen'),
        default=False
    )

    # additional
    attributes = AttributesField(
        verbose_name=_(u'Attributes'),
        blank=True,
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

    video_poster_image = FilerImageField(
        verbose_name=_(u'Video Start Image'),
        related_name='%(app_label)s_%(class)s_video_poster_image',
        help_text=_(
            u'This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.'),
        blank=True,
        null=True
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return self.video_id or self.video_service

    def copy_relations(self, oldinstance):
        self.video_poster_image = oldinstance.video_poster_image

    @property
    def base_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return css_classes

    @property
    def css_classes(self):
        css_classes = self.base_classes
        return ' '.join(css_classes)


@python_2_unicode_compatible
class AllinkVidEmbedPlugin(AllinkVidBasePlugin):
    """
    Renders an Iframe when ``link``
    """

    class Meta:
        verbose_name = _('Allink Video Embed')


    video_id = models.CharField(
        verbose_name=_(u'Video ID'),
        max_length=255,
        help_text=_(u'Only provide the ID. The correct url will be automatically generated.'),
    )
    video_service = models.CharField(
        _(u'Video Service'),
        max_length=50,
        choices=VIDEO_SERVICE_CHOICES,
    )
    ratio = models.CharField(
        _(u'Ratio'),
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.video_id or self.video_service

    # def get_video_dimensions(self):
    #     import sys
    #     from itertools import chain
    #
    #     from hachoir_core.cmd_line import unicodeFilename
    #     from hachoir_metadata import extractMetadata
    #     from hachoir_parser import createParser
    #
    #     if len(sys.argv) != 2:
    #         sys.exit(__doc__)
    #
    #     extractMetadata(self.video_id)
    #     file_metadata = extractMetadata(createParser(unicodeFilename(sys.argv[1])))
    #     width = next((metadata.get('width'), metadata.get('height')) for metadata in chain([file_metadata],
    #     return ("%sx%s" % file_metadata.iterGroups()) if metadata.has('width') and metadata.get('height')))



@python_2_unicode_compatible
class AllinkVidFilePlugin(AllinkVidBasePlugin):
    """
    writes HTML5 <video> tag for video_file
    """

    class Meta:
        verbose_name = _('Allink Video File')

    video_file = FilerFileField(
            verbose_name=_(u'Video File'),
            help_text=_(u'Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>Aspect ratio: TBD<br>File size: Dependent of video length. Generally speaking: Less is more.'),
            on_delete=models.SET_NULL,
            null=True,
            related_name='%(app_label)s_%(class)s_video_file',
    )

    def __str__(self):
        return self.video_file.name
