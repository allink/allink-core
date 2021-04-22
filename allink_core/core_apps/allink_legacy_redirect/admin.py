# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportMixin
from import_export.formats import base_formats

from allink_core.core.utils import base_url
from allink_core.core_apps.allink_legacy_redirect.resources import AllinkLegacyLinkResource
from allink_core.core_apps.allink_legacy_redirect.models import AllinkLegacyLink
from allink_core.core.forms.fields import SelectLinkField
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin


class AllinkLegacyChangeAdminForm(AllinkInternalLinkFieldMixin, forms.ModelForm):
    language = forms.ChoiceField(label='Link Target', required=False,
                                 choices=settings.LANGUAGES)

    new_link = SelectLinkField(label='New Page', required=False)

    class Meta:
        model = AllinkLegacyLink
        fields = ['old', 'overwrite', 'active', 'match_subpages']


class AllinkLegacyLinkAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['old', 'link', 'link_object', 'active', 'match_subpages', 'last_test_result',
                    'last_test_date', 'manual_test']
    readonly_fields = ['last_test_result', 'last_test_date']
    form = AllinkLegacyChangeAdminForm
    resource_class = AllinkLegacyLinkResource
    actions = ['auto_test']
    fields = ['old', 'new_link', 'language', 'overwrite', 'active', 'match_subpages',
              'skip_redirect_when_logged_in', 'last_test_result', 'last_test_date']

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', AllinkLegacyChangeAdminForm)
        return super(AllinkLegacyLinkAdmin, self).get_changelist_form(request, **kwargs)

    def get_import_formats(self):
        """ We only allow csv for
            Google Analytics files
        """
        return [base_formats.CSV]

    def auto_test(self, request, queryset):
        for obj in queryset:
            obj.test_redirect(request)
    auto_test.short_description = 'Test redirect'

    def manual_test(self, obj):
        link = base_url() + obj.old
        return format_html('<a class="button" href="%s" target="_blank">Test</a>' % link)
    manual_test.short_description = 'Manual testing'

    def link_object(self, obj):
        return obj.link_object
    link_object.short_description = 'Page'


admin.site.register(AllinkLegacyLink, AllinkLegacyLinkAdmin)
