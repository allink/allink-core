# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from cms.extensions import TitleExtension
from cms.extensions.extension_pool import extension_pool


# Page Extensions
class AllinkSEOExtension(TitleExtension):
    og_image = FilerImageField(
        verbose_name=_(u'og:Image'),
        help_text=_(
            u'Preview image when page/post is shared on Facebook/ Twitter. <br>Min. 1200 x 630 for best results. If not set, the one from the preview image will be used, if not set or not in a app context, the one defined in allink_settings will be used.'),
        blank=True,
        null=True
    )
    disable_base_title = models.BooleanField(
        _(u'Disable base title'),
        help_text=_(u'If disabled, only the page title will be shown. Everything behind and including the "|" will be removed.'),
        default=False
    )
    override_h1 = models.CharField(
        _(u'Override H1'),
        help_text=_(u'Page Title or App title is default. This option allows you to override the h1 tag.'),
        max_length=255,
        blank=True,
        null=True
    )


extension_pool.register(AllinkSEOExtension)
