# -*- coding: utf-8 -*-
from django.db import models

from cms.models.pluginmodel import CMSPlugin

from allink_core.core.models.fields import CMSPluginField
from allink_core.core.models import AllinkInternalLinkFieldsModel
from allink_core.core.utils import get_additional_templates
from allink_core.core.models.fields_model import AllinkTeaserFieldsModel, AllinkTeaserTranslatedFieldsModel

NEW_WINDOW = 1
SOFTPAGE = 2

TARGET_CHOICES = (
    (NEW_WINDOW, 'New window'),
    (SOFTPAGE, 'Softpage'),
)


class AllinkTeaserPlugin(AllinkInternalLinkFieldsModel, AllinkTeaserFieldsModel, AllinkTeaserTranslatedFieldsModel,
                         CMSPlugin):
    template = models.CharField(
        'Template',
        max_length=50
    )

    link_target = models.IntegerField(
        'Link Target',
        choices=TARGET_CHOICES,
        null=True,
        blank=True
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

    @property
    def softpage_enabled(self):
        return True if self.link_target == SOFTPAGE else False

    @property
    def new_window(self):
        return True if self.link_target == NEW_WINDOW else False

    @property
    def link_attributes(self):
        if self.link_target == NEW_WINDOW:
            return 'target=_blank'
        elif self.link_target == SOFTPAGE:
            return 'data-icon-softpage'
        else:
            return None

    @property
    def link_icon(self):
        if self.link_target == NEW_WINDOW:
            return 'arrow-external'
        elif self.link_target == SOFTPAGE:
            return 'softpage'
        else:
            return None
