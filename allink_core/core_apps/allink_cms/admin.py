# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from cms.extensions import TitleExtensionAdmin

from allink_core.core_apps.allink_cms.models import AllinkSEOExtension

require_POST = method_decorator(require_POST)


@admin.register(AllinkSEOExtension)
class AllinkSEOExtensionAdmin(TitleExtensionAdmin):
    pass
