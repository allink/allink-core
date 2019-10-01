# -*- coding: utf-8 -*-
from django.db import models
from aldryn_translation_tools.models import TranslationHelperMixin
from parler.models import TranslatableModel, TranslatedFieldsModel
from parler.models import TranslatedField
from model_utils.models import TimeStampedModel

from allink_core.core.models.managers import AllinkBaseModelManager
from allink_core.core.models.fields_model import (
    AllinkStatusFieldsModel,
    AllinkSEOFieldsModel,
    AllinkSEOTranslatedFieldsModel,
    AllinkTeaserFieldsModel,
    AllinkTeaserTranslatedFieldsModel,
)
from allink_core.core.models.mixins import (
    AllinkTranslatedAutoSlugifyMixin,
    AllinkInvalidatePlaceholderCacheMixin,
    AllinkMetaTagMixin,
    AllinkTeaserMixin,
    AllinkDetailMixin
)

__all__ = [
    'AllinkBaseTranslatableModel',
    'AllinkBaseTranslatedFieldsModel',
]


class AllinkBaseTranslatableModel(TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin,
                                  AllinkInvalidatePlaceholderCacheMixin, AllinkMetaTagMixin, AllinkTeaserMixin,
                                  AllinkStatusFieldsModel, AllinkDetailMixin, TimeStampedModel, AllinkSEOFieldsModel,
                                  AllinkTeaserFieldsModel, TranslatableModel):
    """
    Base model class for apps with detail view

    - every concrete implementation expects the following attribute:
        slug_source_field_name = 'title'  # does not have to be 'title'

    - get_absolute_url expects a slug field defined

    """

    objects = AllinkBaseModelManager()
    slug = TranslatedField(any_language=True)

    class Meta:
        abstract = True


class AllinkBaseTranslatedFieldsModel(AllinkSEOTranslatedFieldsModel, AllinkTeaserTranslatedFieldsModel,
                                      TranslatedFieldsModel):
    """
    Base model class for apps with detail view
    """

    slug = models.SlugField(
        'Slug',
        max_length=255,
        default='',
        blank=True,
        help_text='Leave blank to auto-generate a unique slug.'
    )

    class Meta:
        abstract = True
