# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.contrib.postgres.fields import ArrayField
from cms.models.pluginmodel import CMSPlugin

from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from allink_core.core.utils import get_additional_templates
from allink_core.core.models.choices import HORIZONTAL_ALIGNMENT_CHOICES, VERTICAL_ALIGNMENT_CHOICES

from settings import ALLOWED_VIDEO_EXTENSIONS


@python_2_unicode_compatible
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
    COL_5 = 'col-5'
    COL_6 = 'col-6'

    # name | verbose_name | column_count
    TEMPLATES = (
        (COL_1, '1 Column', 1, 'col-3-of-3'),
        (COL_1_1, '2 Columns (1:1)', 2, 'col-1-of-2'),
        (COL_2_1, '2 Columns (2:1)', 2, 'col-1-of-3'),
        (COL_1_2, '2 Columns (1:2)', 2, 'col-2-of-3'),
        (COL_3, '3 Columns', 3, 'col-1-of-3'),
        (COL_4, '4 Columns', 4, 'col-1-of-4'),
        (COL_5, '5 Columns', 5, 'col-1-of-5'),
        (COL_6, '6 Columns', 6, 'col-1-of-6'),
    )

    # General Fields
    title = models.CharField(
        _(u'Title'),
        help_text=_(u'The section title'),
        max_length=255,
        blank=True,
        null=True
    )
    title_size = models.CharField(
        _(u'Section Title Size'),
        max_length=50,
    )
    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50
    )
    container_enabled = models.BooleanField(
        _(u'Activate "container"'),
        help_text=_(u'If checked, an inner container with a maximum width is added'),
        default=True
    )
    full_height_enabled = models.BooleanField(
        _(u'Activate "full height" mode'),
        help_text=_(u'If checked, the section will use the available height of the device\'s/browser\'s screen.'),
        default=False
    )
    inverted_colors_enabled = models.BooleanField(
        _(u'Activate "inverted text colors"'),
        help_text=_(u'If checked, the predefined inverted text colors are applied (suitable when using a background image/video)'),
        default=False
    )
    overlay_enabled = models.BooleanField(
        _(u'Activate "overlay"'),
        help_text=_(u'If checked, a predefined overlay background gradient/color is applied.<br><strong>Important:</strong> Only applied when used in combination with a background image/video/color'),
        default=False
    )
    bg_color = models.CharField(
        _(u'Set a predefined background color'),
        max_length=50,
        blank=True,
        null=True
    )
    dynamic_height_enabled = models.BooleanField(
        _(u'Activate dynamic height'),
        help_text=_(u'If checked, the section\'s height will grow depending on the height of its children.<br>Note: This option is being ignored when "full height" or "parallax" are enabled.'),
        default=False
    )
    parallax_enabled = models.BooleanField(
        _(u'Activate Parallax effect'),
        help_text=_(u'If checked, the parallax effect is enabled.'),
        default=False
    )
    bg_image_inner_container = FilerImageField(
        verbose_name=_(u'Background-Image'),
        help_text=_(u'Adds a background image to the inner container of a content section. Activating "overlay styles" is recommended.'),
        related_name="content_container_bg_image",
        blank=True,
        null=True
    )
    bg_image_outer_container = FilerImageField(
        verbose_name=_(u'Background-Image'),
        help_text=_(u'Optional: Set a background image for the content section.<br>Note: This is meant for decorative purposes only and should be used with care.'),
        related_name='%(app_label)s_%(class)s_bg_image',
        blank=True,
        null=True
    )
    # Video related fields
    video_file = FilerFileField(
        verbose_name=_(u'Source'),
        help_text=_(u'Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>File size: Dependent of video length. Generally speaking: Less is more.'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='content_video_file'
    )
    video_poster_image = FilerImageField(
        verbose_name=_(u'Video Start Image'),
        related_name="content_video_poster_image",
        help_text=_(u'This image is displayed while the video is loading. Ideally, use an <strong>exact screen capture image</strong> of the very first frame of the video for best results.'),
        blank=True,
        null=True
    )
    video_mobile_image = FilerImageField(
        verbose_name=_(u'Mobile Image'),
        related_name="content_video_mobile_image",
        help_text=_(u'The image that is being displayed on mobile devices instead of the video.'),
        blank=True,
        null=True
    )
    anchor = models.CharField(
        verbose_name=_(u'ID'),
        max_length=255,
        blank=True,
        help_text=_(u'ID of this content section which can be used for anchor reference from links.<br>'
                    u'Note: Only letters, numbers and hyphen. No spaces or special chars.'),
    )
    ignore_in_pdf = models.BooleanField(
        _(u'Ignore for pdf export'),
        help_text=_(u'If checked, this content section will be ignored when generting a pdf.'),
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
    project_on_screen_effect = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default='default',
    )

    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
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
            choices += ((_(u'Standard'), standard ,), )
            choices += ((_(u'Project'), project, ), )
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
            return u'{} ({})'.format(self.title, self.template)
        else:
            if self.child_plugin_instances:
                for column in self.child_plugin_instances:
                    if column.child_plugin_instances:
                        for plugin in column.child_plugin_instances:
                            if hasattr(plugin, 'title') and plugin.title:
                                return u'... {} ({})'.format(plugin.title, self.template)
                            elif plugin.plugin_type == 'TextPlugin':
                                return u'... {} ({}) ...'.format(strip_tags(plugin.body)[0:50], self.template)
                            elif plugin.plugin_type == 'CMSAllinkImagePlugin':
                                return u'... {} ({}) ...'.format(plugin.picture, self.template)
                            else:
                                return u'({})'.format(self.template)
                    else:
                        return u'({})'.format(self.template)
            else:
                return u'({})'.format(self.template)

    def clean(self):
        if (self.video_file and self.video_file.extension not in ALLOWED_VIDEO_EXTENSIONS):
            raise ValidationError(
                _('Incorrect file type: %(value)s'),
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
        css_classes.append('inner-container-has-bg-image') if self.bg_image_inner_container else None
        # video is stronger than the parallax image
        css_classes.append('parallax-enabled') if self.bg_image_outer_container and self.parallax_enabled and not self.video_file else None

        css_classes.append("has-bg-video") if self.video_file and self.video_poster_image and self.video_mobile_image else None
        # video is stronger than the image
        css_classes.append("has-bg-image") if self.bg_image_outer_container and not self.video_file else None
        css_classes.append("inverted-colors") if self.inverted_colors_enabled else None
        css_classes.append("overlay-enabled") if self.overlay_enabled else None
        css_classes.append("full-height-enabled") if self.full_height_enabled else None
        # "full-height" and "parallax" are stronger than "dynamic-height"
        css_classes.append("dynamic-height-enabled") if self.dynamic_height_enabled and not self.full_height_enabled and not self.parallax_enabled else None
        return ' '.join(css_classes)

    @property
    def attributes(self):
        attributes = []
        if self.project_on_screen_effect:
            attributes.append('data-scroll-spy="{}"'.format(self.project_on_screen_effect))
        return ' '.join(attributes)

    @property
    def section_has_content(self):
        # Property soll True zurueckgeben, wenn eine der folgenden Kritieren zutreffen..
        # - Ein Section Titel gesetzt ist..
        # - Mind. eine Column hat ein Kind
        return True


@python_2_unicode_compatible
class AllinkContentColumnPlugin(CMSPlugin):

    title = models.CharField(
        _(u'Title'),
        max_length=255,
        blank=True,
        null=True
    )
    order_mobile = models.IntegerField(
        _(u'Order Mobile'),
        help_text=_(u'Some columns should be ordered differently on mobile devices when columns are stacked vertically. This option allows you to define the position of the this column.<br><br>Note: Columns ordering is ascending (lowest number displayed first)'),
        blank=True,
        null=True
    )
    alignment_horizontal_mobile = models.CharField(
        _(u'Alignment horizontal mobile'),
        max_length=50,
        choices=HORIZONTAL_ALIGNMENT_CHOICES,
        help_text=_(u'This option overrides the projects default alignment for mobile. (Usually "left")'),
        blank=True,
        null=True
    )
    alignment_horizontal_desktop = models.CharField(
        _(u'Alignment horizontal desktop'),
        max_length=50,
        choices=HORIZONTAL_ALIGNMENT_CHOICES,
        help_text=_(u'This option overrides the projects default alignment for desktop. (Usually "left")'),
        blank=True,
        null=True
    )
    alignment_vertical_desktop = models.CharField(
        _(u'Alignment vertical desktop'),
        max_length=50,
        choices=VERTICAL_ALIGNMENT_CHOICES,
        help_text=_(u'This option overrides the projects default alignment for desktop. (Usually "top")'),
        blank=True,
        null=True
    )

    def __str__(self):
        if self.title and self.template:
            return u'{} ({})'.format(self.title, self.template)
        else:
            return u'({})'.format(self.template)

    def save(self):
        if not self.pk:
            self.order_mobile = self.position
        super(AllinkContentColumnPlugin, self).save()

    @property
    def css_classes(self):
        css_classes = []
        css_classes.append('col-empty') if self.num_children() == 0 else None
        css_classes.append('align-v-desktop-{}'.format(self.alignment_vertical_desktop)) if self.alignment_vertical_desktop else None
        css_classes.append('align-h-desktop-{}'.format(self.alignment_horizontal_desktop)) if self.alignment_horizontal_desktop else None
        css_classes.append('align-h-mobile-{}'.format(self.alignment_horizontal_mobile)) if self.alignment_horizontal_mobile else None
        css_classes.append('col-order-mobile-{}'.format(self.order_mobile))
        return ' '.join(css_classes)

    @property
    def template(self):
        return self.parent.allink_content_allinkcontentplugin.template