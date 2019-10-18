# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import ArrayField
from djangocms_attributes_field.fields import AttributesField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from allink_core.core.models.choices import VIDEO_SERVICE_CHOICES
from allink_core.core.models.fields import CMSPluginField


class AllinkVideoBasePlugin(CMSPlugin):
    attributes = AttributesField(
        verbose_name='Attributes',
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

    cmsplugin_ptr = CMSPluginField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.video_id or self.video_service

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return ' '.join(css_classes)


class AllinkVideoEmbedPlugin(AllinkVideoBasePlugin):
    """
    Renders an Iframe when ``link``
    """

    video_id = models.CharField(
        verbose_name='Video ID',
        max_length=255,
        help_text=('Only provide the ID. The correct URL will automatically be generated.<br><br>'
                   'YouTube: https://www.youtube.com/watch?v=<strong>12345678</strong> '
                   '(the ID is <strong>12345678</strong>)<br>Vimeo: https://vimeo.com/<strong>12345678</strong> '
                   '(the ID is <strong>12345678</strong>)'),
    )
    video_service = models.CharField(
        'Video Service',
        max_length=50,
        choices=VIDEO_SERVICE_CHOICES,
    )
    ratio = models.CharField(
        'Ratio',
        max_length=50,
        blank=True,
        null=True
    )
    auto_start_enabled = models.BooleanField(
        'Autostart',
        default=False,
        help_text='<strong>Important:</strong> Autoplaying videos with audio is not recommended. Use wisely. ',
    )
    allow_fullscreen_enabled = models.BooleanField(
        'Allow fullscreen',
        default=True
    )

    class Meta:
        verbose_name = 'Allink Video Embed'

    def __str__(self):
        return self.video_id or self.video_service


class AllinkVideoFilePlugin(AllinkVideoBasePlugin):
    """
    writes HTML5 <video> tag for video_file
    """

    video_file = FilerFileField(
        verbose_name='Video File',
        on_delete=models.PROTECT,
        help_text=('Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 '
                   '(video loads quick and runs smooth)<br>Audio: Not recommended '
                   '(no audio = smaller file size and less annoyed visitors)<br>File size: '
                   'Dependent of video length. Generally speaking: Less is more.'),
        null=True,
        related_name='%(app_label)s_%(class)s_video_file',
    )
    video_poster_image = FilerImageField(
        verbose_name='Video Start Image',
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_video_poster_image',
        help_text=(
            'Image that is being displayed while the video is loading. '
            'Ideally the very first frame of the video is used, in order to make the transition as smooth as '
            'possible.<br><br><strong>Imoprtant:</strong> Make sure the aspect ratio of the image is '
            '<strong>exactly the same</strong> as the video, otherwise the video height will shrink or grow when the '
            'playback starts.'),
        null=True
    )
    video_file_width = models.IntegerField(
        'Video width',
        blank=True,
        null=True,
    )
    video_file_height = models.IntegerField(
        'Video height',
        blank=True,
        null=True,
    )
    video_muted_enabled = models.BooleanField(
        'Muted',
        help_text='Caution: Autoplaying videos with audio is not recommended. Use wisely.',
        default=True
    )
    poster_only_on_mobile = models.BooleanField(
        'Image Only (Mobile)',
        help_text='Disable video on mobile devices and only show the start image without video control.',
        default=True
    )
    auto_start_enabled = models.BooleanField(
        'Autostart',
        default=True
    )
    auto_start_mobile_enabled = models.BooleanField(
        'Autostart mobile',
        default=False,
        help_text='Caution: Autoplaying videos on mobile is not recommended. Use wisely.',
    )
    allow_fullscreen_enabled = models.BooleanField(
        'Allow fullscreen',
        default=False
    )

    class Meta:
        verbose_name = 'Allink Video File'

    def __str__(self):
        return self.video_file.name

    def copy_relations(self, oldinstance):
        self.video_poster_image = oldinstance.video_poster_image

    # TODO not working yet on stage and production
    # def get_video_dimensions(self):
    #     import subprocess
    #     import shlex
    #     import json
    #
    #     cmd = "avprobe -show_streams -of json"
    #     args = shlex.split(cmd)
    #     args.append(self.video_file.file.path)
    #     avprobeOutput = subprocess.check_output(args).decode('utf-8')
    #     avprobeOutput = json.loads(avprobeOutput)
    #
    #     # find height and width
    #     width = avprobeOutput['streams'][0]['width']
    #     height = avprobeOutput['streams'][0]['height']
    #
    #     return width, height

    # def save(self, no_signals=False, *args, **kwargs):
    # self.video_file_width, self.video_file_height = self.get_video_dimensions()
    # super(AllinkVideoFilePlugin, self).save(*args, **kwargs)
