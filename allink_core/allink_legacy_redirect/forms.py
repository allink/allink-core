# -*- coding: utf-8 -*-
import json

from django import forms

from cms.models import Page

from allink_core.allink_legacy_redirect.models import AllinkLegacyLink
from allink_core.allink_base.models.model_fields import choices_from_sitemaps
from allink_core.allink_base.forms.fields import SelectLinkField
from allink_core.allink_base.forms.widgets import SearchSelectWidget


class AllinkLegacyChangeAdminForm(forms.ModelForm):
    new_page = forms.ChoiceField(choices=())
    additional = SelectLinkField()

    class Meta:
        model = AllinkLegacyLink
        fields = ['old', 'new_page', 'overwrite', 'active', 'match_subpages']

    def __init__(self, *args, **kwargs):
        super(AllinkLegacyChangeAdminForm, self).__init__(*args, **kwargs)
        self.fields['new_page'].choices = choices_from_sitemaps()
        self.fields['additional'].choices = self.fields['additional'].get_page_and_app_choices()
        if self.instance:
            if self.instance.link_page:
                self.fields['additional'].initial = json.dumps({'page_id': self.instance.link_page.id})
            elif self.instance.link_apphook_page:
                self.fields['additional'].initial = json.dumps({
                    'link_apphook_page_id': self.instance.link_apphook_page.id,
                    'link_url_name': self.instance.link_url_name,
                    'link_object_id': self.instance.link_object_id,
                    'link_url_kwargs': self.instance.link_url_kwargs,
                    'link_model': self.instance.link_model
                })

    def save(self, *args, **kwargs):
        # json.dumps({'page_id': p.id}
        # json.dumps({'link_apphook_page_id': p.id, 'link_url_name': url_name, 'link_object_id': obj.id, 'link_url_kwargs': info[1]}
        for field_name, field in filter(lambda x: isinstance(x[1].widget, SearchSelectWidget), self.fields.items()):
            self.save_search_select_field(field_name, field)
        return super(AllinkLegacyChangeAdminForm, self).save(*args, **kwargs)

    def save_search_select_field(self, field_name, field):
        field_data = json.loads(self.cleaned_data[field_name])
        if 'page_id' in field_data:
            self.instance.link_page = Page.objects.get(id=field_data['page_id'])
        else:
            self.instance.link_page = None
            self.instance.link_apphook_page = Page.objects.get(id=field_data['link_apphook_page_id'])
            self.instance.link_object_id = field_data['link_object_id']
            self.instance.link_model = field_data['link_model']
            self.instance.link_url_name = field_data['link_url_name']
            self.instance.link_url_kwargs = field_data['link_url_kwargs']
