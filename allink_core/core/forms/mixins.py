# -*- coding: utf-8 -*-
import json

from django import forms

from cms.models import Page

from allink_core.core.forms.widgets import SearchSelectWidget


class AllinkInternalLinkFieldMixin(forms.ModelForm):
    # additional = SelectLinkField()

    def __init__(self, *args, **kwargs):
        super(AllinkInternalLinkFieldMixin, self).__init__(*args, **kwargs)
        for field_name, field in filter(lambda x: isinstance(x[1].widget, SearchSelectWidget), self.fields.items()):
            self.fields[field_name].choices = self.fields[field_name].get_page_and_app_choices()
            if self.instance:
                if self.instance.link_page:
                    self.fields[field_name].initial = json.dumps({'page_id': self.instance.link_page.id})
                elif self.instance.link_apphook_page:
                    self.fields[field_name].initial = json.dumps({
                        'link_apphook_page_id': self.instance.link_apphook_page.id,
                        'link_url_name': self.instance.link_url_name,
                        'link_object_id': self.instance.link_object_id,
                        'link_url_kwargs': self.instance.link_url_kwargs,
                        'link_model': self.instance.link_model
                    })

    def clean(self):
        cleaned_data = super(AllinkInternalLinkFieldMixin, self).clean()
        for field_name, field in filter(lambda x: isinstance(x[1].widget, SearchSelectWidget), self.fields.items()):
            self.clean_search_select_field(field_name, field, cleaned_data)
        return cleaned_data

    def clean_search_select_field(self, field_name, field, cleaned_data):
        if cleaned_data[field_name]:
            field_data = json.loads(self.cleaned_data[field_name])
            if 'page_id' in field_data:
                self.instance.link_page = Page.objects.get(id=field_data['page_id'])
                self.instance.link_apphook_page = None
                self.instance.link_object_id = None
                self.instance.link_model = None
                self.instance.link_url_name = None
                self.instance.link_url_kwargs = None
            elif 'link_apphook_page_id' in field_data:
                self.instance.link_page = None
                self.instance.link_apphook_page = Page.objects.get(id=field_data['link_apphook_page_id'])
                self.instance.link_object_id = field_data['link_object_id']
                self.instance.link_model = field_data['link_model']
                self.instance.link_url_name = field_data['link_url_name']
                self.instance.link_url_kwargs = field_data['link_url_kwargs']
        else:
            self.instance.link_page = None
            self.instance.link_apphook_page = None
            self.instance.link_object_id = None
            self.instance.link_model = None
            self.instance.link_url_name = None
            self.instance.link_url_kwargs = None
