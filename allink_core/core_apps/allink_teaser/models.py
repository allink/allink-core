# -*- coding: utf-8 -*-
from django.db import models

from cms.models.pluginmodel import CMSPlugin

from allink_core.core.models.fields import CMSPluginField
from allink_core.core.models import AllinkInternalLinkFieldsModel
from allink_core.core.utils import get_additional_templates
from allink_core.core.models.fields_model import AllinkTeaserFieldsModel, AllinkTeaserTranslatedFieldsModel
from allink_core.core.models.base_plugins import AllinkBaseSectionPlugin


class AllinkTeaserGridContainerPlugin(AllinkBaseSectionPlugin):
    COLUMN_ORDERS = AllinkBaseSectionPlugin.COLUMN_ORDERS + (
        ('alternating', 'Alternating'),
    )


class AllinkTeaserPlugin(AllinkInternalLinkFieldsModel, AllinkTeaserFieldsModel, AllinkTeaserTranslatedFieldsModel,
                         CMSPlugin):
    template = models.CharField(
        'Template',
        max_length=50
    )

    softpage_enabled = models.BooleanField(
        'Show detailed information in Softpage',
        help_text='If checked, the detail view of an entry will be displayed in a "softpage".'
                  ' Otherwise the page will be reloaded.',
        default=False
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return '{}'.format(self.link_object)

    @classmethod
    def get_templates(cls):
        templates = ()
        for x, y in get_additional_templates('TEASER'):
            templates += ((x, y),)
        return templates
