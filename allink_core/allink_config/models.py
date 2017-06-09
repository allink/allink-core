# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField
from filer.models.imagemodels import Image
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
        max_length=50,
        blank=True,
        null=True
    )
    mask_icon_color = models.CharField(
        _(u'Mask icon color'),
        help_text=_(u'Mask icon color for safari-pinned-tab.svg'),
        max_length=50,
        blank=True,
        null=True,
    )
    msapplication_tilecolor = models.CharField(
        _(u'msapplication TileColor'),
        help_text=_(u'MS application TitleColor Field'),
        max_length=50,
        blank=True,
        null=True
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
    blog_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
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
    news_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
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
    events_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
    )
    events_registration_verbose = models.CharField(
        _(u'Events Registration verbose name'),
        default=_(u'Event Registration'),
        max_length=255
    )
    events_registration_verbose_plural = models.CharField(
        _(u'Events Registration verbose name plural'),
        default=_(u'Event Registrations'),
        max_length=255
    )
    events_registration_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
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
    locations_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
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
    people_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
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
    testimonial_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
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
    work_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
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
    members_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
    )
    contact_verbose = models.CharField(
        _(u'Contact verbose name'),
        default=_(u'Contact request'),
        max_length=255
    )
    contact_verbose_plural = models.CharField(
        _(u'Contact verbose name plural'),
        default=_(u'Contact requests'),
        max_length=255
    )
    contact_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
    )
    terms_verbose = models.CharField(
        _(u'Terms of Service verbose name'),
        default=_(u'Terms of Service'),
        max_length=255
    )
    terms_verbose_plural = models.CharField(
        _(u'Terms of Service verbose name plural'),
        default=_(u'Terms of Service'),
        max_length=255
    )
    terms_toolbar_enabled = models.BooleanField(
        _(u'Toolbar enabled?'),
        default=True
    )
    google_site_verification = models.CharField(
        _(u'Google Site Verification Code'),
        blank=True,
        null=True,
        max_length=64
    )

    def __str__(self):
        return u'Allink Configuration'

    class Meta:
        verbose_name = _(u'Allink Configuration')

    # SOLO_CACHE does not work in our setup, thats why, we rewrite it here
    def to_dict(self):
        fields = {
            field.name: getattr(self, field.name) for field in self._meta.get_fields() if not isinstance(field, FilerImageField)
        }
        fields.update({
            '%s_id' % (field.name): getattr(self, field.name).id for field in self._meta.get_fields() if isinstance(field, FilerImageField)
        })
        return fields

    def set_to_cache(self):
        cache_key = self.get_cache_key()
        timeout = 60 * 60 * 24 * 180
        cache.set(cache_key, self.to_dict(), timeout)

        # invalidate cache for favicon templatetag
        cache.delete('favicon_context')

    @classmethod
    def get_cache_key(cls):
        prefix = 'solo'
        return '%s:%s' % (prefix, cls.__name__.lower())

    @classmethod
    def get_solo(cls):
        cache_key = cls.get_cache_key()
        obj_dict = cache.get(cache_key)
        if obj_dict:
            obj = cls()
            for name, value in obj_dict.items():
                if name[-3:] == '_id':
                    setattr(obj, name, Image.objects.get(id=value))
                else:
                    setattr(obj, name, value)
        else:
            obj, created = cls.objects.get_or_create(pk=1)
            obj.set_to_cache()
        return obj


from cms.extensions import TitleExtension
from cms.extensions.extension_pool import extension_pool


# Page Extensions
class AllinkMetaTagExtension(TitleExtension):
    og_image = FilerImageField(
        verbose_name=_(u'og:Image'),
        help_text=_(
            u'Preview image when page/post is shared on Facebook/ Twitter. <br>Min. 1200 x 630 for best results. If not set, the one from the preview image will be used, if not set or not in a app context, the one defined in allink_settings will be used.'),
        blank=True,
        null=True
    )
    enable_base_title = models.BooleanField(
        _(u'Enable base title'),
        help_text=_(u'If dsiabled, only the page title will be shown. Everything behind and including the "|" will be removed.'),
        default=True
    )
    override_h1 = models.CharField(
        _(u'Override H1'),
        help_text=_(u'Page Title or App title is default. This option allows you to override the h1 tag.'),
        max_length=255,
        blank=True,
        null=True
    )


extension_pool.register(AllinkMetaTagExtension)
