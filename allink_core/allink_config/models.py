# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.extensions import PageExtension, TitleExtension
from cms.extensions.extension_pool import extension_pool

from filer.fields.image import FilerImageField
from solo.models import SingletonModel

from allink_core.allink_base.models import AllinkMetaTagFieldsModel


class AllinkConfig(SingletonModel):
    default_recipient = models.EmailField(
        _(u'Default recipient E-Mail'),
        null=True,
        blank=True
    )
    default_sender = models.EmailField(
        _(u'Default sender E-Mail'),
        null=True,
        blank=True
    )

    default_og_image = FilerImageField(
        verbose_name=_(u'og:Image'),
        help_text=_(u'Default preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.'),
        blank=True,
        null=True
    )

    def __unicode__(self):
        return _(u'Allink Configuration')

    class Meta:
        verbose_name = _(u'Allink Configuration')


# Page Extensions

class AllinkMetaTagExtension(AllinkMetaTagFieldsModel, TitleExtension):
    pass


extension_pool.register(AllinkMetaTagExtension)


# Unregister existing Plugins
from cms.plugin_pool import plugin_pool
from djangocms_file.cms_plugins import FilePlugin, FolderPlugin


plugin_pool.unregister_plugin(FilePlugin)
plugin_pool.unregister_plugin(FolderPlugin)
