# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
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

Config = get_model('config', 'Config')
AllinkPageExtension = get_model('config', 'AllinkPageExtension')
AllinkTitleExtension = get_model('config', 'AllinkTitleExtension')


class ConfigAdminForm(TranslatableModelForm):
    theme_color = ColorField(label=_('Theme Color'), help_text=_('Theme color for Android Chrome'), required=False)
    mask_icon_color = ColorField(label=_('Mask Icon Color'),
                                 help_text=_('Mask icon color for safari-pinned-tab.svg'), required=False)
    msapplication_tilecolor = ColorField(label=_('MS Application Title Color'),
                                         help_text=_('MS application TitleColor Field'), required=False)

    class Meta(forms.ModelForm):
        model = Config
        exclude = ()


@admin.register(Config)
class ConfigAdmin(TranslatableAdmin, SingletonModelAdmin):
    form = ConfigAdminForm
    change_form_template = 'config/admin/change_form.html'

    class Media:
        js = (
            get_files('djangocms_custom_admin')[1]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[0]['publicPath'],

            )
        }

    def get_fieldsets(self, request, obj=None):

        if get_project_color_choices():
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
                    'google_site_verification',
                )
            }),
        else:
            fieldsets = (_('Site Meta'), {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'default_og_image',
                    'default_base_title',
                    'google_site_verification',
                )
            }),

        fieldsets += (_('Email'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'default_to_email',
                'default_from_email',
            )
        }),

        fieldsets += (_('Newsletter Signup'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'newsletter_lead',
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
