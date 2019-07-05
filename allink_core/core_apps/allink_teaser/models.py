# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from allink_core.core.models.fields import CMSPluginField
from allink_core.core.models import AllinkInternalLinkFieldsModel
from allink_core.core.utils import get_additional_templates
from allink_core.core.models.fields_model import AllinkTeaserFieldsModel, AllinkTeaserTranslatedFieldsModel


class AllinkTeaserPlugin(AllinkInternalLinkFieldsModel, AllinkTeaserFieldsModel, AllinkTeaserTranslatedFieldsModel,
                         CMSPlugin):

    template = models.CharField(
        _('Template'),
        max_length=50
    )

    cmsplugin_ptr = CMSPluginField()

    def __str__(self):
        return u'{}'.format(self.link_object)

    @classmethod
    def get_templates(cls):
        templates = ()
        for x, y in get_additional_templates('TEASER'):
            templates += ((x, y),)
        return templates
