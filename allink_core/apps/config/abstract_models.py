# -*- coding: utf-8 -*-
import pickle
from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import get_language
from cms.extensions import PageExtension, TitleExtension
from menus.menu_pool import menu_pool
from parler.models import TranslatableModel, TranslatedFieldsModel
from parler.utils.context import switch_language
from filer.fields.image import FilerImageField
from solo.models import SingletonModel
from solo import settings as solo_settings
from djangocms_text_ckeditor.fields import HTMLField

from allink_core.core.models import (
    AllinkTeaserFieldsModel,
    AllinkTeaserTranslatedFieldsModel,
    AllinkSEOFieldsModel,
    AllinkSEOTranslatedFieldsModel,
)


class BaseConfig(TranslatableModel, SingletonModel):
    default_og_image = FilerImageField(
        verbose_name='og:image',
        on_delete=models.PROTECT,
        help_text=(
            'Default preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.'),
        blank=True,
        null=True
    )
    theme_color = models.CharField(
        'Theme Color',
        help_text='Theme color for Android Chrome',
        max_length=50,
        blank=True,
        null=True
    )
    mask_icon_color = models.CharField(
        'Mask icon color',
        help_text='Mask icon color for safari-pinned-tab.svg',
        max_length=50,
        blank=True,
        null=True,
    )
    msapplication_tilecolor = models.CharField(
        'msapplication TileColor',
        help_text='MS application TitleColor Field',
        max_length=50,
        blank=True,
        null=True
    )
    google_site_verification = models.CharField(
        'Google Site Verification Code',
        blank=True,
        null=True,
        max_length=64
    )
    default_to_email = models.EmailField(
        'Default to email',
        default='itcrowd@allink.ch',
        max_length=255
    )
    default_from_email = models.EmailField(
        'Default from email',
        default='itcrowd@allink.ch',
        max_length=255
    )

    newsletter_teaser_counter = models.IntegerField(
        'Newsletter Teaser Counter',
        help_text='Number which defines after how many newsentries the newsletter teaser should appear '
                  '(on grid with newsletterteaser). Default is 4',
        default=4,
    )

    class Meta:
        abstract = True
        app_label = 'config'
        verbose_name = 'Configuration'

    def __str__(self):
        return 'Configuration'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from cms.cache import invalidate_cms_page_cache
        invalidate_cms_page_cache()

        # the config is used widely across all apps and cms pages
        cache.clear()

        # invalidate the menu for all sites
        for site in Site.objects.all():
            menu_pool.clear(site_id=site.id)

    def set_to_cache(self):
        """
        saves pickled instance to cache in each language
        """
        for language_code, _ in settings.LANGUAGES:
            cache_key = self.get_cache_key(language_code)
            timeout = getattr(settings, 'SOLO_CACHE_TIMEOUT', solo_settings.SOLO_CACHE_TIMEOUT)
            with switch_language(self, language_code):
                cache.set(cache_key, pickle.dumps(self), timeout)

    @classmethod
    def get_cache_key(cls, language_code):
        """
        e.g: 'solo:config_de'
        """
        return '%s:%s_%s' % ('solo', cls.__name__.lower(), language_code)

    @classmethod
    def get_solo(cls):
        """
        Loads pickled Config instance from cache.
        If it does not already exists in cache, it will get or create it form the database.
        :return:
        Config instance
        """
        cache_key = cls.get_cache_key(get_language())
        obj_dict = cache.get(cache_key)
        if obj_dict:
            obj = pickle.loads(obj_dict)
        if not obj_dict:
            obj, created = cls.objects.get_or_create(pk=cls.singleton_instance_id)
            obj.set_to_cache()
        return obj


class BaseConfigTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(
        'config.Config',
        on_delete=models.CASCADE,
        related_name='translations',
        null=True)

    default_base_title = models.CharField(
        verbose_name='Base title',
        max_length=50,
        help_text=(
            'Default base title, Is also used for default base og:title when page/post is shared on Facebook. <br>'
            'If not supplied the name form Django Sites will be used instead.'),
        blank=True,
        null=True
    )
    newsletter_lead = HTMLField(
        'Newsletter Signup Text',
        help_text='Teaser text in the Newsletter Teaser',
        blank=True,
        null=True,
    )
    newsletter_signup_link = models.URLField(
        'Newsletter Signup Link',
        help_text='Link for Button on Newsletter Teaser',
        blank=True,
        null=True,
    )
    newsletter_declaration_of_consent = HTMLField(
        'Declaration of consent',
        help_text='Detailed declaration of consent.',
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'config'


class BaseAllinkPageExtension(AllinkSEOFieldsModel, AllinkTeaserFieldsModel, PageExtension):
    class Meta:
        abstract = True
        app_label = 'config'


class BaseAllinkTitleExtension(AllinkSEOTranslatedFieldsModel, AllinkTeaserTranslatedFieldsModel, TitleExtension):
    class Meta:
        abstract = True
        app_label = 'config'
