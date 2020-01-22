# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.core.cache import cache

from cms.admin.pageadmin import PageAdmin
from cms.admin.forms import ChangePageForm, AddPageForm
from cms.models.pagemodel import Page
from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin

from solo.admin import SingletonModelAdmin
from webpack_loader.utils import get_files
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from allink_core.core.loading import get_model
from allink_core.core.forms.fields import ColorField
from allink_core.core.utils import get_project_color_choices
from allink_core.core.admin.mixins import AllinkMediaAdminMixin

Config = get_model('config', 'Config')
AllinkPageExtension = get_model('config', 'AllinkPageExtension')
AllinkTitleExtension = get_model('config', 'AllinkTitleExtension')


class ConfigAdminForm(TranslatableModelForm):
    theme_color = ColorField(label='Theme Color', help_text='Theme color for Android Chrome', required=False)
    mask_icon_color = ColorField(label='Mask Icon Color',
                                 help_text='Mask icon color for safari-pinned-tab.svg', required=False)
    msapplication_tilecolor = ColorField(label='MS Application Title Color',
                                         help_text='MS application TitleColor Field', required=False)

    class Meta(forms.ModelForm):
        model = Config
        exclude = ()


@admin.register(Config)
class ConfigAdmin(AllinkMediaAdminMixin, TranslatableAdmin, SingletonModelAdmin):
    form = ConfigAdminForm
    change_form_template = 'config/admin/change_form.html'

    def get_fieldsets(self, request, obj=None):

        if get_project_color_choices():
            fieldsets = ('Site Meta', {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'default_og_image',
                    'default_base_title',
                    'theme_color',
                    'mask_icon_color',
                    'msapplication_tilecolor',
                    'google_site_verification',
                )
            }),
        else:
            fieldsets = ('Site Meta', {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'default_og_image',
                    'default_base_title',
                    'google_site_verification',
                )
            }),

        fieldsets += ('Email', {
            'classes': (
                'collapse',
            ),
            'fields': (
                'default_to_email',
                'default_from_email',
            )
        }),

        fieldsets += ('Newsletter Signup', {
            'classes': (
                'collapse',
            ),
            'fields': (
                'newsletter_lead',
                'newsletter_signup_link',
                'newsletter_teaser_counter',
                'newsletter_declaration_of_consent',
            )
        }),

        return fieldsets

    def clearcache(self, request, object_id):
        cache.clear()
        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def get_urls(self):
        urls = super(ConfigAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            path('clearcache/<int:object_id>/',
                 self.admin_site.admin_view(self.clearcache),
                 name='%s_%s_clearcache' % info
                 )
        ]
        return my_urls + urls


@admin.register(AllinkPageExtension)
class AllinkPageExtensionAdmin(PageExtensionAdmin):
    fieldsets = (
        ('Teaser', {
            'fields': (
                'teaser_image',
            )
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'og_image',
            )
        }),
    )


@admin.register(AllinkTitleExtension)
class AllinkTitleExtensionAdmin(TitleExtensionAdmin):
    fieldsets = (
        ('Teaser', {
            'fields': (
                'teaser_title',
                'teaser_technical_title',
                'teaser_description',
                'teaser_link_text',
            )
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'og_title',
                'og_description',
            )
        }),
    )


"""
We use our own meta fields on the AllinkPageExtension and AllinkTitleExtension models.
So therefore we hide the page_title and the meta_description on the page admin, to reduce confusion.
"""


class AllinkChangePageForm(ChangePageForm):
    page_title = forms.CharField(widget=forms.HiddenInput(), required=False)
    meta_description = forms.CharField(widget=forms.HiddenInput(), required=False)
    menu_title = forms.CharField(widget=forms.HiddenInput(), required=False)


class AllinkAddPageForm(AddPageForm):
    page_title = forms.CharField(widget=forms.HiddenInput(), required=False)
    meta_description = forms.CharField(widget=forms.HiddenInput(), required=False)
    menu_title = forms.CharField(widget=forms.HiddenInput(), required=False)


PageAdmin.form = AllinkAddPageForm
PageAdmin.add_form = AllinkAddPageForm
PageAdmin.change_form = AllinkChangePageForm


admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
