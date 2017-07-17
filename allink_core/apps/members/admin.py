# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from import_export.admin import ImportExportMixin
from parler.admin import TranslatableAdmin
from aldryn_translation_tools.admin import AllTranslationsMixin
from import_export.formats import base_formats

from allink_core.core.loading import get_model, get_class
from allink_core.core_apps.allink_mailchimp.config import MailChimpConfig

config = MailChimpConfig()

Members = get_model('members', 'Members')
MembersLog = get_model('members', 'MembersLog')
MembersResource = get_class('members.resources', 'MembersResource')
MembersAdminForm = get_class('members.forms', 'MembersAdminForm')
send_welcome_email = get_class('members.email', 'send_welcome_email')


class MembersLogAdminInline(admin.TabularInline):
    model = MembersLog
    readonly_fields = ('description', 'created')
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def delete_members(modeladmin, request, queryset):
    for member in queryset:
        member.delete_from_mailchimp_list()
        member.user.delete()


delete_members.short_description = _(u'Delete selected Members (and corresponding Users/ also removes member from mailchimplist)')


def subscribe_members_to_mailchimp(modeladmin, request, queryset):
    for member in queryset:
        member.put_to_mailchimp_list()
        member.log('subscribed_to_mailchimp', u'Member subscribed to Mailchimp-List')


delete_members.subscribe_members_to_mailchimp = _(u'Subscribe member to mailchimplist)')


def send_password_create_email(modeladmin, request, queryset):
    for member in queryset:
        send_welcome_email(request, member)


send_password_create_email.short_description = _(u'Send welcome email')


class MembersAdmin(ImportExportMixin, AllTranslationsMixin, TranslatableAdmin):
    resource_class = MembersResource

    list_display = ('member_nr', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'language')
    inlines = [MembersLogAdminInline]
    readonly_fields = ('user', )
    actions = [send_password_create_email, delete_members, subscribe_members_to_mailchimp]
    form = MembersAdminForm

    def get_actions(self, request):
        actions = super(MembersAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        super(MembersAdmin, self).save_model(request, obj, form, change)

        # update mailchimp list
        obj.put_to_mailchimp_list(form.initial.get('email'))

        if 'email' in form.changed_data:
            obj.log('email_changed_admin', u'Email-Address changed in Django admin.')

        if 'first_name' in form.changed_data:
            obj.log('first_name_changed_admin', u'First name changed in Django admin.')

        if 'last_name' in form.changed_data:
            obj.log('last_name_name_changed_admin', u'Last name changed in Django admin.')

    def get_import_formats(self):
        return [base_formats.XLS]


admin.site.register(Members, MembersAdmin)
