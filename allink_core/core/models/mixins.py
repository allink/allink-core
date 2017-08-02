# -*- coding: utf-8 -*-
from django.db.models import Q
from aldryn_translation_tools.models import TranslatedAutoSlugifyMixin


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
            if not(is_default and self.is_default_slug(new_slug)):
                setattr(self, self.slug_field_name, new_slug)
        # do not call direct superclass, it does the same (but less) again
        return super(TranslatedAutoSlugifyMixin, self).save(**kwargs)