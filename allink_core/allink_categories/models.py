# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from aldryn_translation_tools.models import (
    TranslatedAutoSlugifyMixin, TranslationHelperMixin)
from parler import appsettings
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields
from treebeard.ns_tree import NS_Node, NS_NodeManager, NS_NodeQuerySet


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
class AllinkCategory(TranslatedAutoSlugifyMixin, TranslationHelperMixin,
               TranslatableModel, NS_Node):
    """
      A category is hierarchical. The structure is implemented with django-
      treebeard's Nested Sets trees, which has the performance characteristics
      we're after, namely: fast reads at the expense of write-speed.
      """

    slug_source_field_name = 'name'

    model_names = ArrayField(models.CharField(
        max_length=50),
        help_text=_(u'Please specify the app which uses this categories.'),
        blank=True,
        null=True
    )

    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            blank=False,
            default='',
            max_length=255,
        ),
        slug=models.SlugField(
            _('slug'),
            blank=True,
            default='',
            help_text=_('Provide a “slug” or leave blank for an automatically '
                        'generated one.'),
            max_length=255,
        ),
        meta={'unique_together': (('language_code', 'slug', ), )}
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    objects = CategoryManager()

    def delete(self, using=None):
        #
        # We're simply managing how the two superclasses perform deletion
        # together here.
        #
        self.__class__.objects.filter(pk=self.pk).delete(using)
        super(TranslatableModel, self).delete()

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)
