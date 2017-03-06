# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin

from allink_core.allink_base.models.model_fields import Classes, Icon, CMSPluginField
from allink_core.allink_base.models.reusable_fields import AllinkLinkFieldsModel
from allink_core.allink_base.models import choices

from . import model_fields

@python_2_unicode_compatible
class AllinkButtonLinkContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for Links, Buttons
    """

    def __str__(self):
        return _(u'{}').format(str(self.pk))


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

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return u'{}'.format(self.label)
