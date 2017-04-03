# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from aldryn_translation_tools.models import TranslationHelperMixin

from parler import appsettings
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields, TranslatableModelMixin
from parler.cache import _delete_cached_translations
from treebeard.ns_tree import NS_Node, NS_NodeManager, NS_NodeQuerySet

from allink_core.allink_base.models.mixins import AllinkTranslatedAutoSlugifyMixin


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

    def not_root(self, depth=2):
        return self.filter(depth__gte=depth)

    if django.VERSION < (1, 8):
        get_query_set = get_queryset


@python_2_unicode_compatible
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
        help_text=_(u'Please specify the app which uses this categories. All apps specified in parent category are automatically added.'),
        blank=True,
        null=True
    )

    # used to decide if it should be possible to use
    # this category in a filter on a specific plugin.
    # all categories with the same tag can be used
    # in the same filter.
    tag = models.CharField(
        _(u'Tag'),
        max_length=80,
        help_text=_(u'auto-generated categories use this tag, to identify which app generated the category.'),
        # choices=settings.PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES,
        null=True,
        blank=True
    )

    translations = TranslatedFields(
        name=models.CharField(
            _(u'name'),
            blank=False,
            default='',
            max_length=255,
        ),
        slug=models.SlugField(
            _(u'slug'),
            blank=True,
            default='',
            help_text=_('Provide a “slug” or leave blank for an automatically '
                        'generated one.'),
            max_length=255,
        ),
        meta={'unique_together': (('language_code', 'slug', ), )}
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    objects = CategoryManager()

    def delete(self, using=None):
        #
        # We're simply managing how the two superclasses perform deletion
        # together here.
        #
        self.__class__.objects.filter(pk=self.pk).delete(using)
        _delete_cached_translations(self)
        super(TranslatableModelMixin, self).delete()

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)
