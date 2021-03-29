# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField
from filer.fields.image import FilerFileField

from aldryn_translation_tools.models import TranslationHelperMixin

from parler import appsettings
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields, TranslatableModelMixin
from parler.cache import _delete_cached_translations
from treebeard.ns_tree import NS_Node, NS_NodeManager, NS_NodeQuerySet

from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin


LANGUAGE_CODES = appsettings.PARLER_LANGUAGES.get_active_choices()


class CategoryQuerySet(TranslatableQuerySet, NS_NodeQuerySet):
    pass


class CategoryManager(TranslatableManager, NS_NodeManager):
    queryset_class = CategoryQuerySet

    def get_queryset(self):
        return self.queryset_class(
            self.model,
            using=self._db
        ).order_by('tree_id', 'lft')

    def not_root(self, depth=100):
        return self.filter(depth__gte=depth)


class AllinkCategory(AllinkTranslatedAutoSlugifyMixin, TranslationHelperMixin,
                     TranslatableModel, NS_Node):
    """
      A category is hierarchical. The structure is implemented with django-
      treebeard's Nested Sets trees, which has the performance characteristics
      we're after, namely: fast reads at the expense of write-speed.
      """

    slug_source_field_name = 'name'

    model_names = ArrayField(models.CharField(
        max_length=50),
        help_text=('Please specify the app which uses this categories. '
                   'All apps specified in parent category are automatically added.'),
        blank=True,
        null=True
    )

    # used to decide if it should be possible to use
    # this category in a filter on a specific plugin.
    # all categories with the same tag can be used
    # in the same filter.
    tag = models.CharField(
        'Tag',
        max_length=80,
        help_text='auto-generated categories use this tag, to identify which app generated the category.',
        null=True,
        blank=True
    )

    logo = FilerFileField(
        verbose_name='Logo',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_logo',
    )

    # the verbose counterpart to field 'tag' (iidentifier can and has to be set manually)
    # as a addition to make queries on categories (for example to create filter slect dropdown in app plugins)
    identifier = models.CharField(
        'Identifier',
        max_length=50,
        help_text='Identifier used for backward reference on a app model. '
                  '(e.g display category name on People app, e.g Marketing)',
        blank=True,
        null=True
    )

    translations = TranslatedFields(
        name=models.CharField(
            'name',
            blank=False,
            default='',
            max_length=255,
        ),
        slug=models.SlugField(
            'slug',
            blank=True,
            default='',
            help_text=('Provide a “slug” or leave blank for an automatically '
                        'generated one.'),
            max_length=255,
        ),
        meta={'unique_together': [('language_code', 'slug')]},
    )

    objects = CategoryManager()

    class Meta:
        app_label = 'allink_categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    def delete(self, using=None):
        #
        # We're simply managing how the two superclasses perform deletion
        # together here.
        #
        self.__class__.objects.filter(pk=self.pk).delete(using)
        _delete_cached_translations(self)
        super(TranslatableModelMixin, self).delete()
