# -*- coding: utf-8 -*-
from aldryn_translation_tools.models import TranslationHelperMixin
from parler.models import TranslatableModel, TranslatedFieldsModel
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

    - every concrete implementation expects at least the following fields:
        slug_source_field_name = 'title'  # does not have to be 'title'

        title = TranslatedField(any_language=True)  # does not have to be 'title'
        slug = TranslatedField(any_language=True)

    - get_absolute_url expects a slug field defined

    """

    objects = AllinkBaseModelManager()

    class Meta:
        abstract = True


class AllinkBaseTranslatedFieldsModel(AllinkSEOTranslatedFieldsModel, AllinkTeaserTranslatedFieldsModel,
                                      TranslatedFieldsModel):
    """
    Base model class for apps with detail view
    """
    class Meta:
        abstract = True
