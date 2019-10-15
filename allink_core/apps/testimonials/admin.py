# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from adminsortable.admin import SortableAdmin
from allink_core.core.loading import get_model
from parler.admin import TranslatableAdmin
from allink_core.core.admin import AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, \
    AllinkTeaserAdminMixin


Testimonials = get_model('testimonials', 'Testimonials')


@admin.register(Testimonials)
class TestimonialsAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, AllinkTeaserAdminMixin,
                        TranslatableAdmin, SortableAdmin):
    search_fields = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name', 'status', 'all_categories_column', 'created', 'modified')

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    ('first_name', 'last_name'),
                    'lead',
                    'slug',
                    'preview_image',
                    'job_function',
                    'company_name',
                ),
            }),
        )
        fieldsets += self.get_category_fieldsets()
        fieldsets += self.get_teaser_fieldsets()
        fieldsets += self.get_seo_fieldsets()
        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
        return super(TestimonialsAdmin, self).formfield_for_dbfield(db_field, **kwargs)
