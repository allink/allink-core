# -*- coding: utf-8 -*-
from aldryn_translation_tools.models import TranslatedAutoSlugifyMixin


class AllinkManualEntriesMixin(object):

    def get_category_navigation(self):
        category_navigation = []
        # if manual entries are selected the category navigation
        # is created from all distinct categories in selected entries
        if self.manual_entries.count() > 0:
            for entry in self.manual_entries.all():
                for category in entry.categories.all():
                    if category not in category_navigation:
                        category_navigation.append(category)
        else:
            # override auto category nav
            if self.category_navigation.count() > 0:
                for category in self.category_navigation.all():
                    if self.get_render_queryset_for_display(category).exists():
                        category_navigation.append(category)
            # auto category nav
            else:
                for category in self.categories.all():
                    if self.get_render_queryset_for_display(category).exists():
                        category_navigation.append(category)
        return category_navigation

    def copy_relations(self, oldinstance):
        self.categories = oldinstance.categories.all()
        self.category_navigation = oldinstance.category_navigation.all()
        self.manual_entries = oldinstance.manual_entries.all()

    def get_selected_entries(self, filters={}):
        return self.manual_entries.active().filter(**filters)

    def get_render_queryset_for_display(self, category=None, filters={}):
        """
         returns all data_model objects distinct to id which are in the selected categories
          - category: category instance
          - filters: dict model fields and value
            -> adds additional query

        -> Is also defined in  AllinkManualEntriesMixin to handel manual entries !!
        """

        # apply filters from request
        queryset = self.data_model.objects.filter(**filters)

        if self.categories.count() > 0 or category:
            """
             category selection
            """
            if category:
                queryset = queryset.filter_by_category(category)
                if self.categories_and.count() > 0:
                    queryset = queryset.filter(categories=self.categories_and.all())
            else:
                queryset = queryset.filter_by_categories(self.categories.all())
                if self.categories_and.count() > 0:
                    queryset = queryset.filter(categories=self.categories_and.all())
            return self._apply_ordering_to_queryset_for_display(queryset)

        else:
            queryset = queryset.active_entries()
            return queryset


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
