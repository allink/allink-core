# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.plugin_pool import plugin_pool
from cms.extensions import PageExtension, TitleExtension
from parler.models import TranslatableModel, TranslatedFieldsModel
from filer.fields.image import FilerImageField
from django.utils.translation import get_language
from filer.models.imagemodels import Image
from solo.models import SingletonModel
from djangocms_text_ckeditor.fields import HTMLField


@python_2_unicode_compatible
class BaseConfig(SingletonModel, TranslatableModel):
    default_og_image = FilerImageField(
        verbose_name=_(u'og:image'),
        help_text=_(
            u'Default preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.'),
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
    gallery_plugin_caption_text_max_length = models.IntegerField(
        _(u'Gallery Plugin max length of caption text Field'),
        blank=True,
        null=True,
    )
    google_site_verification = models.CharField(
        _(u'Google Site Verification Code'),
        blank=True,
        null=True,
        max_length=64
    )
    default_to_email = models.EmailField(
        _(u'Default to email'),
        default='itcrowd@allink.ch',
        max_length=255
    )
    default_from_email = models.EmailField(
        _(u'Default from email'),
        default='itcrowd@allink.ch',
        max_length=255
    )

    class Meta:
        abstract = True
        app_label = 'config'
        verbose_name = _(u'Configuration')

    def __str__(self):
        return u'Configuration'

        # SOLO_CACHE does not work in our setup, thats why, we rewrite it here

    def to_dict(self):
        fields = {
            field.name: getattr(self, field.name) for field in self._meta.get_fields() if
        not isinstance(field, FilerImageField) and field.name != 'translations'
        }
        fields.update({
            '%s_id' % (field.name): getattr(self, field.name).id for field in self._meta.get_fields() if
        getattr(self, field.name) and isinstance(field, FilerImageField)
        })
        try:
            fields.update({
                field.name: getattr(self.get_translation(get_language()), field.name) for field in
            self.translations.model._meta.get_fields() if field.name not in ['master', 'language_code']
            })
        except self.translations.model.DoesNotExist:
            self.create_translation(get_language(), default_base_title='')
            fields.update({
                field.name: getattr(self, field.name) for field in self.translations.model._meta.get_fields() if
            field.name not in ['master', 'language_code']
            })
        return fields

    def set_to_cache(self, language_code=None):
        language_code = get_language() if not language_code else language_code
        cache_key = self.get_cache_key(language_code)
        timeout = 60 * 60 * 24 * 180
        cache.set(cache_key, self.to_dict(), timeout)


    def save(self, *args, **kwargs):

        self.pk = 1

        for language_code, language in settings.LANGUAGES:
            self.set_to_cache(language_code)

        # invalidate cache for favicon templatetag
        cache.delete('favicon_context')
        super(SingletonModel, self).save(*args, **kwargs)

        # we need to invalidate all placeholder cache keys,
        # where a plugin is placed that displayes data from this model
        # adapted from cms/models/pagemodel.py
        from cms.cache import invalidate_cms_page_cache
        invalidate_cms_page_cache()

        relevant_models = (self.__class__,) + self.__class__.__bases__
        relevant_plugin_classes = [x for x in plugin_pool.get_all_plugins() if
                                   hasattr(x.model, 'data_model') and x.model.data_model in relevant_models]

        # get all pages where a relevant plugin is placed
        for plugin_class in relevant_plugin_classes:
            for plugin in plugin_class.model.objects.all():
                for language_code, language in settings.LANGUAGES:
                    if plugin.page:
                        plugin.placeholder.clear_cache(language_code, site_id=plugin.page.site_id)

    @classmethod
    def get_cache_key(cls, language_code=None):
        language_code = get_language() if not language_code else language_code
        prefix = 'solo'
        return '%s:%s_%s' % (prefix, cls.__name__.lower(), language_code)

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
            try:
                obj = cls.objects.get(pk=1)
                obj.set_to_cache()
            except cls.DoesNotExist:
                obj = cls.objects.create()
                obj.create_translation(get_language(), default_base_title='')
                obj.set_to_cache()
            except:
                return None
        return obj


class BaseConfigTranslation(TranslatedFieldsModel):
    master = models.ForeignKey('config.Config', related_name='translations', null=True)

    default_base_title = models.CharField(
        verbose_name=_(u'Base title'),
        max_length=50,
        help_text=_(
            u'Default base title, Is also used for default base og:title when page/post is shared on Facebook. <br>If not supplied the name form Django Sites will be used instead.'),
        blank=True,
        null=True
    )
    newsletter_lead = HTMLField(
        _(u'Newsletter Signup Text'),
        help_text=_(u'Teaser text in the newsletter signup view (data usage explainer).'),
        blank=True,
        null=True,
    )
    newsletter_declaration_of_consent = HTMLField(
        _(u'Declaration of consent'),
        help_text=_(u'Detailed declaration of consent.'),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'config'


# Page Extensions
class BaseAllinkPageExtension(PageExtension):
    special_subnav_enabled = models.BooleanField(
        _(u'Special Subnav enabled?'),
        default=False
    )

    class Meta:
        abstract = True
        app_label = 'config'


# Title  Extensions
class BaseAllinkTitleExtension(TitleExtension):

    class Meta:
        abstract = True
        app_label = 'config'
