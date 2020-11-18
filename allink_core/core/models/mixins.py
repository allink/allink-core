# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import NoReverseMatch
from django.utils.translation import ugettext_lazy as _, override
from menus.menu_pool import menu_pool
from cms.utils.i18n import get_current_language, get_default_language
from cms.plugin_pool import plugin_pool
from aldryn_translation_tools.models import TranslatedAutoSlugifyMixin
from allink_core.core.loading import get_model

__all__ = [
    'AllinkDetailMixin',
    'AllinkTranslatedAutoSlugifyMixin',
    'AllinkInvalidatePlaceholderCacheMixin',
    'AllinkMetaTagMixin',
]


class AllinkDetailMixin:
    """
    Mixin for models with detail view

    - always used in combination with aldryn_translation_tools.models.TranslationHelperMixin
    """

    def get_detail_view(self, application_namespace=None):
        """
        :param application_namespace:
        an application_namespace, e.g 'news'
        - this is usually supplied, when calling from a app_content plugin with a specific apphook
        :return:
        fully qualified detail view identifier, e.g 'news:detail'
        """
        if application_namespace:
            return '{}:detail'.format(application_namespace)
        else:
            return '{}:detail'.format(self._meta.app_label)

    def get_absolute_url(self, language=None, application_namespace=None):
        """
        :param language:
        :param application_namespace:
        :return:

        """
        from django.urls import reverse
        if not language:
            language = get_current_language() or get_default_language()

        slug, language = self.known_translation_getter('slug', None, language_code=language)
        try:
            with override(language):
                return reverse(self.get_detail_view(application_namespace), kwargs={'slug': slug})
        except NoReverseMatch:
            # so we can spot this common problem also when not in DEBUG mode.
            return '/no_apphook_configured'


class AllinkTranslatedAutoSlugifyMixin(TranslatedAutoSlugifyMixin):
    """
    This is a TranslatableModel mixin that automatically generates a suitable
    slug for the object on save.
    If `slug_globally_unique` is True, then slugs will be required to be
    unique across all languages.
    If `slug_globally_unique` is False (default), then the strategy used here
    is that it is OK for two objects to use the same slug if the slugs are for
    different languages. So if this were used on an Article model, these would
    be valid:
        /en/pain -> Article in EN about physical discomfort
        /fr/pain -> Article in FR about bread
    Of course, this means that when resolving an object from its URL, care must
    be taken to factor in the language segment of the URL too.

    The allink version of this Mixin adds the functionality, that with each
    save we try to change the slug if it is a default slug. To a more specific one.

    This is especially useful for auto-generated categories, which get a default
    slug during creation.
    """

    def is_default_slug(self, slug):
        return slug and self.get_slug_default() in slug

    def save(self, **kwargs):
        slug = self._get_existing_slug()
        is_default = self.is_default_slug(slug)
        if not slug or self._slug_exists(slug) or is_default:
            new_slug = self.make_new_slug(slug=slug if not is_default else None)

            # we do not want to change a default slug to a new default slug
            if not (is_default and self.is_default_slug(new_slug)):
                setattr(self, self.slug_field_name, new_slug)
        # do not call direct superclass, it does the same (but less) again
        return super(TranslatedAutoSlugifyMixin, self).save(**kwargs)


class AllinkInvalidatePlaceholderCacheMixin:
    """
    This Mixin is used in combination with a CMS-Plugin. It makes sure that the placeholder cache keys get deleted,
    when the involved model instance is saved.

    The Plugin must define a attribute 'data_model', otherwise it won't get deleted.
    e.g:
        class HistoryPlugin(CMSPlugin):
            data_model = HistoryItem


    Only the placeholder caches get deleted, which contain relevant plugins.

    """

    def save(self, *args, **kwargs):
        super(AllinkInvalidatePlaceholderCacheMixin, self).save(*args, **kwargs)
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
                    plugin.placeholder.clear_cache(language_code, site_id=getattr(plugin.page, 'site_id', None))

        # invalidate the menu for all sites
        for site in Site.objects.all():
            menu_pool.clear(site_id=site.id)


class AllinkMetaTagMixin:
    """
    Mixin for all relevant meta fields. Defines the fallback hierarchy.

    Used in combination with:

    AllinkTeaserFieldsModel,
    AllinkTeaserTranslatedFieldsModel,
    AllinkSEOFieldsModel,
    AllinkSEOTranslatedFieldsModel,

    """

    META_FIELD_FALLBACK_CONF = {
        'meta_image': [
            {'model': 'self', 'field': 'og_image', },
            {'model': 'self', 'field': 'teaser_image', },
            {'model': 'self', 'field': 'preview_image', },
            {'model': 'config.Config', 'field': 'default_og_image', },
        ],
        'meta_title': [
            {'model': 'self', 'field': 'og_title', },
            {'model': 'self', 'field': 'teaser_title', },
            {'model': 'self', 'field': 'title', },
        ],
        'meta_description': [
            {'model': 'self', 'field': 'og_description', },
            {'model': 'self', 'field': 'teaser_description', },
            {'model': 'self', 'field': 'lead', },
        ]
    }

    @property
    def field_fallback_conf(self):
        """
        the get_fallback function is interested in both META_FIELD_FALLBACK_CONF and TEASER_FIELD_FALLBACK_CONF
        but it is not guaranteed, that AllinkMetaTagMixin and AllinkTeaserMixin are used together.
        """
        try:
            return {**self.META_FIELD_FALLBACK_CONF, **self.TEASER_FIELD_FALLBACK_CONF}
        except AttributeError:
            return self.TEASER_FIELD_FALLBACK_CONF

    @property
    def meta_image_thumb(self):
        """
        We always want the meta image with a maximum width of 1200px. The ratio should be preserved.
        :return:
        image object
        """
        from allink_core.apps.config.utils import get_fallback, generate_meta_image_thumb
        meta_image = get_fallback(self, 'meta_image')
        return generate_meta_image_thumb(meta_image)

    @property
    def meta_page_title(self):
        from allink_core.apps.config.utils import get_fallback
        Config = get_model('config', 'Config')
        allink_config = Config.get_solo()

        base_title = ' | ' + getattr(allink_config, 'default_base_title', '')
        page_title = get_fallback(self, 'meta_title')

        return page_title + base_title

    @property
    def meta_dict(self):
        """
        :return:
        dict with all relevant meta fields
        e.g. used for seo template snippet: templatetags/allink_meta_og.html
        """
        from allink_core.apps.config.utils import get_fallback

        Config = get_model('config', 'Config')
        allink_config = Config.get_solo()

        meta_context = {
            'meta_page_title': self.meta_page_title,
            'meta_og_title': get_fallback(self, 'meta_title'),
            'meta_description': get_fallback(self, 'meta_description'),
            'meta_image_url': getattr(self.meta_image_thumb, 'url', ''),
            'google_site_verification': allink_config.google_site_verification,
        }
        return meta_context


class AllinkTeaserMixin:
    """
    Mixin for all relevant teaser fields. Defines the fallback hierarchy.

    Used in combination with:

    AllinkTeaserFieldsModel,
    AllinkTeaserTranslatedFieldsModel


    override TEASER_FIELD_FALLBACK_CONF on per app basis:
    ...
    """

    TEASER_LINK_TEXT = _('Read more')

    TEASER_FIELD_FALLBACK_CONF = {
        'teaser_image': [
            {'model': 'self', 'field': 'teaser_image', },
            {'model': 'self', 'field': 'preview_image', },
        ],
        'teaser_title': [
            {'model': 'self', 'field': 'teaser_title', },
            {'model': 'self', 'field': 'title', },
        ],
        'teaser_technical_title': [
            {'model': 'self', 'field': 'teaser_technical_title', },
        ],
        'teaser_description': [
            {'model': 'self', 'field': 'teaser_description', },
            {'model': 'self', 'field': 'lead', },
        ],
        'teaser_link_text': [
            {'model': 'self', 'field': 'teaser_link_text', },
            {'model': 'self', 'field': 'TEASER_LINK_TEXT', },
        ],
        'teaser_link_url': [
            {'model': 'self', 'field': 'teaser_link_url', },
        ],
        # If you adjust this don't forget to adjust the TEASER_FIELD_FALLBACK_CONF in all apps where
        # TEASER_FIELD_FALLBACK_CONF is overridden!
    }

    @property
    def field_fallback_conf(self):
        """
        the get_fallback function is interested in both META_FIELD_FALLBACK_CONF and TEASER_FIELD_FALLBACK_CONF
        but it is not guaranteed, that AllinkMetaTagMixin and AllinkTeaserMixin are used together.
        """
        try:
            return {**self.META_FIELD_FALLBACK_CONF, **self.TEASER_FIELD_FALLBACK_CONF}
        except AttributeError:
            return self.TEASER_FIELD_FALLBACK_CONF

    @property
    def teaser_dict(self):
        """
        :return:
        dict with all relevant teaser fields
        e.g. used for teaser templates e.g: allink_teaser/<<template_name>>/item.html
        """
        from allink_core.apps.config.utils import get_fallback

        teaser_context = {
            'teaser_title': get_fallback(self, 'teaser_title'),
            'teaser_technical_title': get_fallback(self, 'teaser_technical_title'),
            'teaser_description': get_fallback(self, 'teaser_description'),
            'teaser_image': get_fallback(self, 'teaser_image'),
            'teaser_link_text': get_fallback(self, 'teaser_link_text'),
            'teaser_link': self.get_absolute_url(),
            'teaser_link_url': get_fallback(self, 'teaser_link_url'),
        }
        return teaser_context
