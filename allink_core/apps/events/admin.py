# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin
from allink_core.core.admin import AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, \
    AllinkTeaserAdminMixin, AllinkCategoryAdminForm
from allink_core.core.loading import get_model
from allink_core.core.utils import get_additional_choices

Events = get_model('events', 'Events')
EventsRegistration = get_model('events', 'EventsRegistration')


class EventsContentAdminForm(AllinkCategoryAdminForm):

    def __init__(self, *args, **kwargs):
        super(EventsContentAdminForm, self).__init__(*args, **kwargs)

        if get_additional_choices('ADDITIONAL_EVENTS_DETAIL_TEMPLATES'):
            self.fields['template'] = forms.CharField(
                label=_('Template'),
                widget=forms.Select(choices=get_additional_choices('ADDITIONAL_EVENTS_DETAIL_TEMPLATES', blank=True)),
                required=False,
            )
        else:
            self.fields['template'] = forms.CharField(widget=forms.HiddenInput(), required=False)


@admin.register(Events)
class EventsAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin,
                  AllinkTeaserAdminMixin, PlaceholderAdminMixin,
                  TranslatableAdmin):
    form = EventsContentAdminForm
    list_display = ('title', 'status', 'all_categories_column', 'entry_date',)

    # entry_date = forms.DateTimeField(
    #     label=_('Date and Time'),
    #     widget=forms.widgets.DateTimeInput(
    #         attrs={
    #             'placeholder': _('Please choose date and time'),
    #             'data-dateFormat': 'Y-m-d H:i',
    #             'data-altFormat': 'D, j. F Y, H:i',
    #             'data-minDate': str(datetime.date.today() - datetime.timedelta(days=180)),
    #             'data-maxDate': 'today',
    #             'data-enableTime': True,
    #         }
    #     ),
    # )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
        return super(EventsAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    'title',
                    'slug',
                    'template',
                    'preview_image',
                    ('entry_date', 'costs',),
                    'lead',
                    'location',
                    'form_enabled',
                    'created',
                )
            }),
        )

        fieldsets += (
            ('Published From/To', {
                'classes': ('collapse',),
                'fields': (
                    'start',
                    'end',
                )
            }),
        )
        fieldsets += self.get_category_fieldsets()
        fieldsets += self.get_seo_fieldsets()
        return fieldsets


@admin.register(EventsRegistration)
class EventsRegistrationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'created', 'event', 'message',)
    list_filter = ('event',)
