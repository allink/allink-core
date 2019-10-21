# -*- coding: utf-8 -*-
"""
use core:
from allink_core.apps.dummy_app.models import *  # noqa

if you overwrite, you don't have to override every model.
"""
from django.db import models
from parler.models import TranslatedField
from allink_core.apps.dummy_app.abstract_models import BaseDummyApp, BaseDummyAppTranslation, BaseDummyAppAppContentPlugin
from allink_core.core.loading import get_model


class DummyApp(BaseDummyApp):
    some_field = models.IntegerField(null=True)

    some_field_translated_field = TranslatedField(any_language=True)


class DummyAppTranslation(BaseDummyAppTranslation):
    some_field_translated_field = models.IntegerField(null=True)


class DummyAppAppContentPlugin(BaseDummyAppAppContentPlugin):
    data_model = get_model('dummy_app', 'DummyApp')
    some_plugin_field = models.IntegerField(null=True)


from allink_core.apps.dummy_app.models import *  # noqa
