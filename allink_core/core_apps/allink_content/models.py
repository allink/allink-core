# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.contrib.postgres.fields import ArrayField
from cms.models.pluginmodel import CMSPlugin

from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from allink_core.core.utils import get_additional_templates
from allink_core.core.models.choices import HORIZONTAL_ALIGNMENT_CHOICES, VERTICAL_ALIGNMENT_CHOICES
from allink_core.core.models.fields import CMSPluginField


class AllinkContentPlugin(CMSPlugin):
    """
    A plugin representing different column-counts
    and special option for rendering its container-content compared to its Content-Plugins background-image.
    """

    COL_1 = 'col-1'
    COL_1_1 = 'col-1-1'
    COL_2_1 = 'col-2-1'
    COL_1_2 = 'col-1-2'
    COL_3 = 'col-3'
    COL_4 = 'col-4'

    # name | verbose_name | column_count
    TEMPLATES = (
        (COL_1, '1 Column', 1, 'col-3-of-3'),
        (COL_1_1, '2 Columns (1:1)', 2, 'col-1-of-2'),
        (COL_2_1, '2 Columns (2:1)', 2, 'col-1-of-3'),
        (COL_1_2, '2 Columns (1:2)', 2, 'col-2-of-3'),
        (COL_3, '3 Columns', 3, 'col-1-of-3'),
        (COL_4, '4 Columns', 4, 'col-1-of-4'),
    )

    # General Fields
    title = models.CharField(
        'Title',
        help_text='The section title',
        max_length=255,
        blank=True,
        null=True
    )
    title_size = models.CharField(
        'Section Title Size',
        max_length=50,
    )
    template = models.CharField(
        'Template',
        help_text='Choose a template.',
        max_length=50
    )
    container_enabled = models.BooleanField(
        'Activate "container"',
        help_text='If checked, an inner container with a maximum width is added',
        default=True
    )
    inverted_colors_enabled = models.BooleanField(
        'Activate "inverted text colors"',
        help_text=('If checked, the predefined inverted text colors are applied '
                   '(suitable when using a background image/video)'),
        default=False
    )
    overlay_enabled = models.BooleanField(
        'Activate "overlay"',
        help_text=('If checked, a predefined overlay background gradient/color is applied.<br>'
                   '<strong>Important:</strong> Only applied when used in combination with a background '
                   'image/video/color'),
        default=False
    )
    bg_color = models.CharField(
        'Set a predefined background color',
        max_length=50,
        blank=True,
        null=True
    )
    dynamic_height_enabled = models.BooleanField(
        'Activate dynamic height',
        help_text=('If checked, the section\'s height will grow depending on the height of its children.<br>Note: '
                   'This option is being ignored when "full height" or "parallax" are enabled.'),
        default=False
    )
    bg_image_outer_container = FilerImageField(
        verbose_name='Background-Image',
        on_delete=models.PROTECT,
        help_text='Optional: Set a background image for the content section.',
        related_name='%(app_label)s_%(class)s_bg_image',
        blank=True,
        null=True
    )
    # Video related fields
    video_file = FilerFileField(
        verbose_name='Source',
        on_delete=models.PROTECT,
        help_text=('Recommended video settings:<br><br>Format: '
                   'mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: '
                   'Not recommended (no audio = smaller file size and less annoyed visitors)<br>File size: '
                   'Dependent of video length. Generally speaking: Less is more.'),
        blank=True,
        null=True,
        related_name='content_video_file'
    )
    video_poster_image = FilerImageField(
        verbose_name='Video Start Image',
        on_delete=models.PROTECT,
        related_name="content_video_poster_image",
        help_text=('This image is displayed while the video is loading. Ideally, use an '
                   '<strong>exact screen capture image</strong> of the very first frame of the video for best '
                   'results.'),
        blank=True,
        null=True
    )
    video_mobile_image = FilerImageField(
        verbose_name='Mobile Image',
        on_delete=models.PROTECT,
        related_name="content_video_mobile_image",
        help_text='The image that is being displayed on mobile devices instead of the video.',
        blank=True,
        null=True
    )
    anchor = models.CharField(
        verbose_name='ID',
        max_length=255,
        blank=True,
        help_text=('ID of this content section which can be used for anchor reference from links.<br>'
                   'Note: Only letters, numbers and hyphen. No spaces or special chars.'),
    )
    ignore_in_pdf = models.BooleanField(
        'Ignore for pdf export',
        help_text='If checked, this content section will be ignored when generting a pdf.',
        default=False
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

    project_css_spacings_top_bottom = models.CharField(
        'Spacings',
        help_text='Choose a spacing (top and bottom).',
        max_length=50,
        blank=True,
        null=True
    )
    project_css_spacings_top = models.CharField(
        'Spacings top',
        help_text='Choose a top spacing.',
        max_length=50,
        blank=True,
        null=True
    )
    project_css_spacings_bottom = models.CharField(
        'Spacings bottom',
        help_text='Choose a bottom spacing.',
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_templates(cls):
        templates = cls.TEMPLATES
        for a, b, c, d in get_additional_templates('ADDITIONAL_CONTENT'):
            templates += ((a, b, c, d),)
        return templates

    @classmethod
    def get_additional_templates(cls):
        templates = ()
        for a, b, c, d in get_additional_templates('ADDITIONAL_CONTENT'):
            templates += ((a, b, c, d),)
        return templates

    @classmethod
    def get_template_choices(cls):
        choices = ()
        standard = ()
        project = ()

        for template in cls.TEMPLATES:
            standard += ((template[0], template[1]),)

        for template in cls.get_additional_templates():
            project += ((template[0], template[1]),)

        if project:
            choices += (('Standard', standard,),)
            choices += (('Project', project,),)
        else:
            choices = standard

        return choices

    @classmethod
    def get_template_column_count(cls, name):
        for template in cls.get_templates():
            if template[0] == name:
                return template[2]

    def get_short_description(self):
        """
         for better overview in structure mode
         display title, if supplied. if not supplied either display the first title of the first child plugin.
         If the first child has no title and there is a Text Plugin, display the first character of the TextPlugin.
        """
        if self.title:
            return'{} ({})'.format(self.title, self.template)
        else:
            if self.child_plugin_instances:
                for column in self.child_plugin_instances:
                    if column.child_plugin_instances:
                        for plugin in column.child_plugin_instances:
                            if hasattr(plugin, 'title') and plugin.title:
                                return'... {} ({})'.format(plugin.title, self.template)
                            elif plugin.plugin_type == 'TextPlugin':
                                return'... {} ({}) ...'.format(strip_tags(plugin.body)[0:50], self.template)
                            elif plugin.plugin_type == 'CMSAllinkImagePlugin':
                                return'... {} ({}) ...'.format(plugin.picture, self.template)
                            else:
                                return'({})'.format(self.template)
                    else:
                        return'({})'.format(self.template)
            else:
                return'({})'.format(self.template)

    def clean(self):
        if self.video_file and self.video_file.extension not in settings.ALLOWED_VIDEO_EXTENSIONS:
            raise ValidationError(
                'Incorrect file type: %(value)s',
                params={'value': self.video_file.extension},
            )

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        css_classes.append('first') if self.position == 0 else None
        css_classes.append("container-enabled") if self.container_enabled else None
        css_classes.append('section-heading-{}'.format(self.title_size)) if self.title_size else None
        css_classes.append("has-bg-color") if self.bg_color else None
        css_classes.append(self.bg_color) if self.bg_color else None
        css_classes.append("has-bg-video") \
            if self.video_file and self.video_poster_image and self.video_mobile_image else None
        # video is stronger than the image
        css_classes.append("has-bg-image") if self.bg_image_outer_container and not self.video_file else None
        css_classes.append("inverted-colors") if self.inverted_colors_enabled else None
        css_classes.append("overlay-enabled") if self.overlay_enabled else None
        css_classes.append("dynamic-height-enabled") \
            if self.dynamic_height_enabled else None
        css_classes.append("dynamic-height-enabled") if self.dynamic_height_enabled else None
        return ' '.join(css_classes)

    @property
    def css_section_classes(self):
        css_classes = []
        if self.project_css_spacings_top:
            css_classes.append('{}-top'.format(self.project_css_spacings_top))
        if self.project_css_spacings_bottom:
            css_classes.append('{}-bottom'.format(self.project_css_spacings_bottom))
        if self.project_css_spacings_top_bottom:
            css_classes = self.project_css_spacings_top_bottom
            return css_classes
        return ' '.join(css_classes)

    @property
    def attributes(self):
        attributes = []
        return ' '.join(attributes)


class AllinkContentColumnPlugin(CMSPlugin):
    title = models.CharField(
        'Title',
        max_length=255,
        blank=True,
        null=True
    )
    order_mobile = models.IntegerField(
        'Order Mobile',
        help_text=('Some columns should be ordered differently on mobile devices when columns are '
                   'stacked vertically. This option allows you to define the position of the this column.<br><br>'
                   'Note: Columns ordering is ascending (lowest number displayed first)'),
        blank=True,
        null=True
    )
    alignment_horizontal_mobile = models.CharField(
        'Alignment horizontal mobile',
        max_length=50,
        choices=HORIZONTAL_ALIGNMENT_CHOICES,
        help_text='This option overrides the projects default alignment for mobile. (Usually "left")',
        blank=True,
        null=True
    )
    alignment_horizontal_desktop = models.CharField(
        'Alignment horizontal desktop',
        max_length=50,
        choices=HORIZONTAL_ALIGNMENT_CHOICES,
        help_text='This option overrides the projects default alignment for desktop. (Usually "left")',
        blank=True,
        null=True
    )
    alignment_vertical_desktop = models.CharField(
        'Alignment vertical desktop',
        max_length=50,
        choices=VERTICAL_ALIGNMENT_CHOICES,
        help_text='This option overrides the projects default alignment for desktop. (Usually "top")',
        blank=True,
        null=True
    )

    def __str__(self):
        if self.title and self.template:
            return '{} ({})'.format(self.title, self.template)
        else:
            return '({})'.format(self.template)

    @property
    def css_classes(self):
        css_classes = []
        css_classes.append('col-empty') if self.num_children() == 0 else None
        css_classes.append('align-v-desktop-{}'.format(self.alignment_vertical_desktop)) \
            if self.alignment_vertical_desktop else None
        css_classes.append('align-h-desktop-{}'.format(self.alignment_horizontal_desktop)) \
            if self.alignment_horizontal_desktop else None
        css_classes.append('align-h-mobile-{}'.format(self.alignment_horizontal_mobile)) \
            if self.alignment_horizontal_mobile else None
        css_classes.append('col-order-mobile-{}'.format(self.order_mobile))
        return ' '.join(css_classes)

    @property
    def template(self):
        try:
            return self.parent.allink_content_allinkcontentplugin.template
        except AttributeError:
            # a AllinkContentColumnPlugin should always have a parent and therefore a template.
            # But when copied, the parent isn't set yet.
            return 'no template'
