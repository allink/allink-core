# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.postgres.fields import ArrayField
from django.utils.http import urlquote
from cms.models.pluginmodel import CMSPlugin

from allink_core.core.models.fields import Icon, CMSPluginField
from allink_core.core.models.models import AllinkLinkFieldsModel
from allink_core.core.models import choices

from allink_core.core_apps.allink_button_link import model_fields


@python_2_unicode_compatible
class AllinkButtonLinkContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for Links, Buttons
    """
    alignment_horizontal_desktop = models.CharField(
        _(u'Alignment horizontal desktop'),
        max_length=50,
        choices=choices.HORIZONTAL_ALIGNMENT_CHOICES,
        help_text=_(u'This option overrides the projects default alignment for desktop. (Usually "left")'),
        blank=True,
        null=True
    )
    alignment_horizontal_mobile = models.CharField(
        _(u'Alignment horizontal mobile'),
        max_length=50,
        choices=choices.HORIZONTAL_ALIGNMENT_CHOICES,
        help_text=_(u'This option overrides the projects default alignment for mobile. (Usually "left")'),
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
        return _(u'{}').format(str(self.pk))

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


@python_2_unicode_compatible
class AllinkButtonLinkPlugin(CMSPlugin, AllinkLinkFieldsModel):
    label = models.CharField(
        verbose_name=_(u'Display name'),
        blank=True,
        default='',
        max_length=255,
    )
    type = model_fields.LinkOrButton(
        verbose_name=_(u'Type'),
    )
    # button specific fields
    btn_context = model_fields.Context(
        verbose_name=_(u'Context'),
        choices=choices.BUTTON_CONTEXT_CHOICES,
        default=choices.BUTTON_CONTEXT_DEFAULT,
    )
    btn_size = model_fields.Size(
        verbose_name=_(u'Size'),
    )
    btn_block = models.BooleanField(
        verbose_name=_(u'Block'),
        default=False,
    )
    # text link specific fields
    txt_context = model_fields.Context(
        verbose_name=_(u'Context'),
        choices=choices.TEXT_LINK_CONTEXT_CHOICES,
        default=choices.TEXT_LINK_CONTEXT_DEFAULT,
        blank=True,
    )
    # common fields
    icon_left = Icon(
        verbose_name=_(u'Icon left'),
    )
    icon_right = Icon(
        verbose_name=_(u'Icon right'),
    )

    # email specific fields
    email_subject = models.CharField(
        verbose_name=_(u'Subject'),
        max_length=255,
        default='',
        blank=True,
    )
    email_body_text = models.TextField(
        verbose_name=_(u'Body Text'),
        default='',
        blank=True,
    )
    # form specific fields
    send_internal_mail = models.BooleanField(
        _(u'Send internal e-mail'),
        default=True,
        help_text=_(u'Send confirmation mail to defined internal e-mail addresses.')
    )
    internal_email_addresses = ArrayField(
        models.EmailField(
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
        verbose_name=_(u'Internal e-mail addresses'),
    )
    from_email_address = models.EmailField(
        _(u'Sender e-mail address'),
        blank=True,
        null=True
    )
    send_external_mail = models.BooleanField(
        _(u'Send external e-mail'),
        default=True,
        help_text=_(u'Send confirmation mail to customer.')
    )
    thank_you_text = models.TextField(
        _(u'Thank you text'),
        blank=True,
        null=True,
        help_text=_(u'This text will be shown, after form completion.')
    )
    label_layout = models.CharField(
        _(u'Display labels'),
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

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return u'{}'.format(self.label)

    def get_link_url(self):
        base = super(AllinkButtonLinkPlugin, self).get_link_url()
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
