# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from cms.extensions import TitleExtensionAdmin
from solo.admin import SingletonModelAdmin

from .models import AllinkConfig, AllinkMetaTagExtension

require_POST = method_decorator(require_POST)

@admin.register(AllinkConfig)
class ConfigAdmin(SingletonModelAdmin):
    pass


@admin.register(AllinkMetaTagExtension)
class AllinkMetaTagExtensionAdmin(TitleExtensionAdmin):
    pass
