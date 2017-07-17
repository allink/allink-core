# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from allink_core.core.loading import get_model
from allink_core.core.admin import AllinkBaseAdminSortable

Testimonials = get_model('testimonials', 'Testimonials')


@admin.register(Testimonials)
class TestimonialsAdmin(AllinkBaseAdminSortable):
    search_fields = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name', 'get_categories', 'is_active', 'created', 'modified')

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'is_active',
                    ('first_name', 'last_name'),
                    'lead',
                    'slug',
                    'created',
                    'preview_image',
                ),
            }),
        )

        fieldsets += self.get_base_fieldsets()

        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
        return super(TestimonialsAdmin, self).formfield_for_dbfield(db_field, **kwargs)
