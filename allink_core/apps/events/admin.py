# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from cms.admin.placeholderadmin import PlaceholderAdminMixin


from allink_core.core.admin import AllinkBaseAdminSortable
from allink_core.core.admin import AllinkBaseAdminForm
from allink_core.core_apps.allink_categories.models import AllinkCategory
from allink_core.core.loading import get_model
from allink_core.core.utils import get_additional_choices

Events = get_model('events', 'Events')
EventsRegistration = get_model('events', 'EventsRegistration')


class EventsContentAdminForm(AllinkBaseAdminForm):

    def __init__(self, *args, **kwargs):
        super(EventsContentAdminForm, self).__init__(*args, **kwargs)
        self.fields['categories'].initial = AllinkCategory.objects.not_root().filter(translations__name__iexact=self._meta.model._meta.model_name)

        if get_additional_choices('ADDITIONAL_EVENTS_DETAIL_TEMPLATES'):
            self.fields['template'] = forms.CharField(
                label=_(u'Template'),
                widget=forms.Select(choices=get_additional_choices('ADDITIONAL_EVENTS_DETAIL_TEMPLATES', blank=True)),
                required=False,
            )
        else:
            self.fields['template'] = forms.CharField(widget=forms.HiddenInput(), required=False)



@admin.register(Events)
class EventsAdmin(PlaceholderAdminMixin, AllinkBaseAdminSortable):
    form = EventsContentAdminForm
    list_display = ('title', 'get_categories', 'event_date_time', 'status', )
    # event_date_time = forms.DateTimeField(
    #     label=_(u'Date and Time'),
    #     widget=forms.widgets.DateTimeInput(
    #         attrs={
    #             'placeholder': _(u'Please choose date and time'),
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
                    ('event_date_time', 'costs', ),
                    'lead',
                    'location',
                    'form_enabled',
                    'created',
                ),
            }),
        )

        fieldsets += (_('Published From/To'), {
            'classes': ('collapse',),
            'fields': (
                'start',
                'end',
            )
        }),

        fieldsets += self.get_base_fieldsets()
        return fieldsets


@admin.register(EventsRegistration)
class EventsRegistrationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'created', 'event', 'message',)
    list_filter = ('event', )
