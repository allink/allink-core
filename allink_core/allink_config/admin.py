# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _


from cms.extensions import TitleExtensionAdmin
from solo.admin import SingletonModelAdmin

from allink_core.allink_config.models import AllinkConfig, AllinkMetaTagExtension

require_POST = method_decorator(require_POST)


@admin.register(AllinkConfig)
class AllinkConfigAdmin(SingletonModelAdmin):

    def get_fieldsets(self, request, obj=None):

        fieldsets = (_('Site Meta'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'default_og_image',
                'default_base_title',
                'theme_color',
                'mask_icon_color',
                'msapplication_tilecolor',
            )
        }),

        fieldsets += (_('App Names'), {
            'classes': (
                'collapse',
            ),
            'description': _(u'Please notice that the plugin names will only change after restarting the server.(Please redeploy with Divio Cloud Dashboard.)'),
            'fields': (
                ('blog_verbose', 'blog_verbose_plural',),
                ('news_verbose', 'news_verbose_plural',),
                ('events_verbose', 'events_verbose_plural',),
                ('locations_verbose', 'locations_verbose_plural',),
                ('members_verbose', 'members_verbose_plural',),
                ('people_verbose', 'people_verbose_plural',),
                ('testimonial_verbose', 'testimonial_verbose_plural',),
                ('work_verbose', 'work_verbose_plural',),
            )
        }),

        return fieldsets


@admin.register(AllinkMetaTagExtension)
class AllinkMetaTagExtensionAdmin(TitleExtensionAdmin):
    pass
