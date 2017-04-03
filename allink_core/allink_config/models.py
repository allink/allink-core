# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from cms.extensions import TitleExtension
from cms.extensions.extension_pool import extension_pool
from cms.plugin_pool import plugin_pool
from djangocms_file.cms_plugins import FilePlugin, FolderPlugin

from filer.fields.image import FilerImageField
from solo.models import SingletonModel

from allink_core.allink_base.models import AllinkMetaTagFieldsModel


@python_2_unicode_compatible
class AllinkConfig(SingletonModel):

    default_og_image = FilerImageField(
        verbose_name=_(u'og:image'),
        help_text=_(u'Default preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.'),
        blank=True,
        null=True
    )
    default_base_title = models.CharField(
        verbose_name=_(u'Base title'),
        max_length=50,
        help_text=_(u'Default base title, Is also used for default base og:title when page/post is shared on Facebook. <br>If not supplied the name form Django Sites will be used instead.'),
        blank=True,
        null=True
    )
    theme_color = models.CharField(
        _(u'Theme Color'),
        help_text=_(u'Theme color for Android Chrome'),
        default='#ffffff',
        max_length=7
    )
    mask_icon_color = models.CharField(
        _(u'Mask icon color'),
        help_text=_(u'Mask icon color for safari-pinned-tab.svg'),
        default='#282828',
        max_length=7
    )
    msapplication_tilecolor = models.CharField(
        _(u'msapplication TileColor'),
        help_text=_(u'MS application TitleColor Field'),
        default='#282828',
        max_length=7
    )

    blog_verbose = models.CharField(
        _(u'Blog verbose name'),
        default=_(u'Blog entry'),
        max_length=255
    )

    blog_verbose_plural = models.CharField(
        _(u'Blog verbose name plural'),
        default=_(u'Blog'),
        max_length=255
    )

    news_verbose = models.CharField(
        _(u'News verbose name'),
        default=_(u'News entry'),
        max_length=255
    )

    news_verbose_plural = models.CharField(
        _(u'News verbose name plural'),
        default=_(u'News'),
        max_length=255
    )

    events_verbose = models.CharField(
        _(u'Events verbose name'),
        default=_(u'Event'),
        max_length=255
    )

    events_verbose_plural = models.CharField(
        _(u'Events verbose name plural'),
        default=_(u'Events'),
        max_length=255
    )

    locations_verbose = models.CharField(
        _(u'Locations verbose name'),
        default=_(u'Location'),
        max_length=255
    )

    locations_verbose_plural = models.CharField(
        _(u'Locations verbose name plural'),
        default=_(u'Locations'),
        max_length=255
    )

    members_verbose = models.CharField(
        _(u'Members verbose name'),
        default=_(u'Member'),
        max_length=255
    )

    members_verbose_plural = models.CharField(
        _(u'Members verbose name plural'),
        default=_(u'Members'),
        max_length=255
    )

    people_verbose = models.CharField(
        _(u'People verbose name'),
        default=_(u'Person'),
        max_length=255
    )

    people_verbose_plural = models.CharField(
        _(u'People verbose name plural'),
        default=_(u'People'),
        max_length=255
    )

    testimonial_verbose = models.CharField(
        _(u'Testimonials verbose name'),
        default=_(u'Testimonial'),
        max_length=255
    )

    testimonial_verbose_plural = models.CharField(
        _(u'Testimonials verbose name plural'),
        default=_(u'Testimonials'),
        max_length=255
    )

    work_verbose = models.CharField(
        _(u'Work verbose name'),
        default=_(u'Project/ Reference'),
        max_length=255
    )

    work_verbose_plural = models.CharField(
        _(u'Work verbose name plural'),
        default=_(u'Projects/ References'),
        max_length=255
    )

    def __str__(self):
        return u'Allink Configuration'

    class Meta:
        verbose_name = _(u'Allink Configuration')


# Page Extensions
class AllinkMetaTagExtension(AllinkMetaTagFieldsModel, TitleExtension):
    pass


extension_pool.register(AllinkMetaTagExtension)


# Unregister existing Plugins

plugin_pool.unregister_plugin(FilePlugin)
plugin_pool.unregister_plugin(FolderPlugin)
