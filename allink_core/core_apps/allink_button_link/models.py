# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property
from django.utils.http import urlquote

from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from allink_core.core.models.fields import Icon, CMSPluginField
from allink_core.core.models import AllinkLinkFieldsModel
from allink_core.core.models import choices

from allink_core.core_apps.allink_button_link import model_fields


class AllinkButtonLinkContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for Links, Buttons
    """
    alignment_horizontal_desktop = models.CharField(
        _('Alignment horizontal desktop'),
        max_length=50,
        choices=choices.HORIZONTAL_ALIGNMENT_CHOICES,
        help_text=_('This option overrides the projects default alignment for desktop. (Usually "left")'),
        blank=True,
        null=True
    )
    alignment_horizontal_mobile = models.CharField(
        _('Alignment horizontal mobile'),
        max_length=50,
        choices=choices.HORIZONTAL_ALIGNMENT_CHOICES,
        help_text=_('This option overrides the projects default alignment for mobile. (Usually "left")'),
        blank=True,
        null=True
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

    def __str__(self):
        return _('{}').format(str(self.pk))

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        css_classes.append('align-h-desktop-{}'.format(
            self.alignment_horizontal_desktop)) if self.alignment_horizontal_desktop else None
        css_classes.append(
            'align-h-mobile-{}'.format(self.alignment_horizontal_mobile)) if self.alignment_horizontal_mobile else None
        return ' '.join(css_classes)


class AllinkButtonLinkPlugin(CMSPlugin, AllinkLinkFieldsModel):

    DEFAULT_LINK = 'default_link'
    FILE_LINK = 'file_link'
    IMAGE_LINK = 'image_link'
    PHONE_LINK = 'phone_link'
    EMAIL_LINK = 'email_link'
    FORM_LINK = 'form_link'
    VIDEO_EMBEDDED_LINK = 'video_embedded_link'
    VIDEO_FILE_LINK = 'video_file_link'

    TEMPLATE_CHOICES = (
        (DEFAULT_LINK, _('Internal/External')),
        (FILE_LINK, _('File (Download)')),
        (IMAGE_LINK, _('Image')),
        (PHONE_LINK, _('Phone')),
        (EMAIL_LINK, _('Email')),
        (FORM_LINK, _('Form')),
        (VIDEO_EMBEDDED_LINK, _('Video (Embedded)')),
        (VIDEO_FILE_LINK, _('Video (File)')),
    )

    # we re-use the template option to toggle fieldset visibility depending on the link types
    template = models.CharField(
        _('Link type'),
        help_text=_('Choose a link type in order to display its options below.'),
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default=DEFAULT_LINK
    )
    label = models.CharField(
        verbose_name=_('Link text'),
        blank=True,
        default='',
        max_length=255,
    )
    type = model_fields.LinkOrButton(
        verbose_name=_('Display type'),
    )
    # button specific fields
    btn_context = model_fields.Context(
        verbose_name=_('Variation'),
        choices=choices.BUTTON_CONTEXT_CHOICES,
        default=choices.BUTTON_CONTEXT_DEFAULT,
    )
    btn_size = model_fields.Size(
        verbose_name=_('Size'),
    )
    btn_block = models.BooleanField(
        verbose_name=_('Block'),
        default=False,
    )
    # text link specific fields
    txt_context = model_fields.Context(
        verbose_name=_('Context'),
        choices=choices.TEXT_LINK_CONTEXT_CHOICES,
        default=choices.TEXT_LINK_CONTEXT_DEFAULT,
        blank=True,
    )
    # common fields
    icon_left = Icon(
        verbose_name=_('Icon left'),
    )
    icon_right = Icon(
        verbose_name=_('Icon right'),
    )

    # email specific fields
    email_subject = models.CharField(
        verbose_name=_('Subject'),
        max_length=255,
        default='',
        blank=True,
    )
    email_body_text = models.TextField(
        verbose_name=_('Body Text'),
        default='',
        blank=True,
    )
    # form specific fields
    send_internal_mail = models.BooleanField(
        _('Send internal e-mail'),
        default=False,
        help_text=_('Send confirmation mail to defined internal e-mail addresses.')
    )
    internal_email_addresses = ArrayField(
        models.EmailField(
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
        verbose_name=_('Internal e-mail addresses'),
    )
    from_email_address = models.EmailField(
        _('Sender e-mail address'),
        blank=True,
        null=True
    )
    send_external_mail = models.BooleanField(
        _('Send external e-mail'),
        default=False,
        help_text=_('Send confirmation mail to customer.')
    )
    thank_you_text = models.TextField(
        _('Thank you text'),
        blank=True,
        null=True,
        help_text=_('This text will be shown, after form completion.')
    )
    label_layout = models.CharField(
        _('Display labels'),
        max_length=15,
        choices=(
            ('stacked', 'Stacked with fields'),
            ('side_by_side', 'Side by side with fields'),
            ('placeholder', 'As placeholders'),
        ),
        default='stacked',
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
    # video (embed) specific fields
    video_id = models.CharField(
        verbose_name=_('Video ID'),
        max_length=255,
        help_text=_(
            u'Only provide the ID. The correct URL will automatically be generated.<br><br>'
            u'YouTube: https://www.youtube.com/watch?v=<strong>12345678</strong> '
            u'(the ID is <strong>12345678</strong>)<br>Vimeo: https://vimeo.com/<strong>12345678</strong> '
            u'(the ID is <strong>12345678</strong>)'),
        blank=True,
        null=True,
    )
    video_service = models.CharField(
        _('Video Service'),
        max_length=50,
        choices=choices.VIDEO_SERVICE_CHOICES,
        blank=True,
        null=True,
    )
    ratio = models.CharField(
        _('Ratio'),
        max_length=50,
        blank=True,
        null=True
    )

    # video (file) specific fields
    video_file = FilerFileField(
        verbose_name=_('Video File'),
        on_delete=models.PROTECT,
        help_text=_(
            u'Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 '
            u'(video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less '
            u'annoyed visitors)<br>File size: Dependent of video length. Generally speaking: Less is more.'),
        blank=True,
        null=True,
        related_name='%(app_label)s_%(class)s_video_file',
    )
    video_poster_image = FilerImageField(
        verbose_name=_('Video Start Image'),
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_video_poster_image',
        help_text=_(
            u'Image that is being displayed while the video is loading. Ideally the very first frame of the video '
            u'is used, in order to make the transition as smooth as possible.<br><br><strong>Imoprtant:</strong> '
            u'Make sure the aspect ratio of the image is <strong>exactly the same</strong> as the video, '
            u'otherwise the video height will shrink or grow when the playback starts.'),
        blank=True,
        null=True,
    )
    video_muted_enabled = models.BooleanField(
        _('Muted'),
        help_text=_('Caution: Autoplaying videos with audio is not recommended. Use wisely.'),
        default=True
    )
    # video (embed and file) specific fields
    auto_start_enabled = models.BooleanField(
        _('Autostart'),
        default=False,
        help_text=_('<strong>Important:</strong> Autoplaying videos with audio is not recommended. Use wisely. '),
    )
    allow_fullscreen_enabled = models.BooleanField(
        _('Allow fullscreen'),
        default=True
    )
    # modal closing options
    data_modal_escape_close_enabled = models.BooleanField(
        _('Escape key closes modal'),
        default=True,
    )
    data_modal_overlay_close_enabled = models.BooleanField(
        _('Click on overlay closes modal'),
        default=True,
    )
    data_modal_button_close_enabled = models.BooleanField(
        _('Display close button'),
        default=True,
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return u'{}'.format(self.label)

    @cached_property
    def link_url_typed(self):
        base = super(AllinkButtonLinkPlugin, self).link_url_typed
        link = base
        if self.link_mailto:
            parameters = {}
            if self.email_subject:
                parameters = {'subject': urlquote(self.email_subject)}
            if self.email_body_text:
                parameters['body'] = urlquote(self.email_body_text)
            link = '{}?{}'.format(base, '&'.join('{}={}'.format(v, k) for (v, k) in parameters.items()))
        return link

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        css_classes.append('side-by-side') if self.label_layout == 'side_by_side' else None
        css_classes.append('placeholder-enabled') if self.label_layout == 'placeholder' else None
        return ' '.join(css_classes)
