# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.shortcuts import redirect
from django.conf.urls import url

from parler.admin import TranslatableAdmin

from allink_core.core_apps.allink_terms.models import AllinkTerms


@admin.register(AllinkTerms)
class AllinkTermsAdmin(TranslatableAdmin, admin.ModelAdmin):
    list_display = ('__str__', 'status', 'start', 'end')
    fields = ('text', 'terms_cms_page')
    actions = None
    change_form_template = 'allink_terms/admin/change_form.html'

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.is_publishable:
            return False
        return super(AllinkTermsAdmin, self).has_delete_permission(request, obj)

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = []
        return super(AllinkTermsAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        instance = self.get_object(request, unquote(object_id))
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_as_new'] = False
        extra_context['hide_save_and_add_another'] = True
        extra_context['hide_save_and_continue'] = True
        if instance and instance.status != AllinkTerms.STATUS_DRAFT:
            self.readonly_fields = ['text', 'terms_cms_page']
        else:
            self.readonly_fields = []
        return super(AllinkTermsAdmin, self).change_view(request, object_id, form_url, extra_context)

    def publish(self, request, object_id):
        instance = self.get_object(request, object_id)
        if instance:
            instance.publish()
        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def get_urls(self):
        urls = super(AllinkTermsAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            url(
                r'^(.+)/publish/$',
                self.admin_site.admin_view(self.publish),
                name='%s_%s_publish' % info
            )
        ]
        return my_urls + urls
