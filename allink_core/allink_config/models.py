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


# Unregister existing Plugins TODO
from cms.plugin_pool import plugin_pool
from aldryn_bootstrap3.cms_plugins import Bootstrap3SpacerCMSPlugin, Bootstrap3IconCMSPlugin, \
    Bootstrap3AccordionCMSPlugin, Bootstrap3AlertCMSPlugin, Bootstrap3BlockquoteCMSPlugin, \
    Bootstrap3CarouselCMSPlugin, Bootstrap3FileCMSPlugin, Bootstrap3ColumnCMSPlugin, Bootstrap3LabelCMSPlugin,\
    Bootstrap3ImageCMSPlugin, Bootstrap3ButtonCMSPlugin
from djangocms_link.cms_plugins import LinkPlugin
from djangocms_file.cms_plugins import FilePlugin, FolderPlugin
from djangocms_snippet.cms_plugins import SnippetPlugin

# plugin_pool.unregister_plugin(Bootstrap3ButtonCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3IconCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3AccordionCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3AlertCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3BlockquoteCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3CarouselCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3FileCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3ColumnCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3SpacerCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3LabelCMSPlugin)
plugin_pool.unregister_plugin(Bootstrap3ImageCMSPlugin)

plugin_pool.unregister_plugin(LinkPlugin)
plugin_pool.unregister_plugin(FilePlugin)
plugin_pool.unregister_plugin(FolderPlugin)
plugin_pool.unregister_plugin(SnippetPlugin)
