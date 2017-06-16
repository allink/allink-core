# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.postgres.fields import ArrayField
from django.utils.http import urlquote
from cms.models.pluginmodel import CMSPlugin

from allink_core.allink_base.models.model_fields import Classes, Icon, CMSPluginField
from allink_core.allink_base.models.reusable_fields import AllinkLinkFieldsModel
from allink_core.allink_base.models import choices

from allink_core.djangocms_button_link import model_fields


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
    def base_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return css_classes

    @property
    def css_classes(self):
        css_classes = self.base_classes
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
    extra_css_classes = Classes()

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

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return u'{}'.format(self.label)

    @property
    def get_link_url(self):
        base = super(AllinkButtonLinkPlugin, self).get_link_url()
        parameters = {}
        if self.link_mailto:
            if self.email_subject:
                parameters = {'subject': urlquote(self.email_subject)}
            if self.email_body_text:
                parameters['body'] = urlquote(self.email_body_text)
        return '{}?{}'.format(base, '&'.join('{}={}'.format(v, k) for (v, k) in parameters.items()))
