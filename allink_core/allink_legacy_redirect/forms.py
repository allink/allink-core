# -*- coding: utf-8 -*-
from django import forms

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

    def save(self, *args, **kwargs):
        # json.dumps({'page_id': p.id}
        # json.dumps({'link_apphook_page_id': p.id, 'link_url_name': url_name, 'link_object_id': obj.id, 'link_url_kwargs': info[1]}
        for field_name, field in filter(lambda x: isinstance(x[1].widget, SearchSelectWidget), self.fields.items()):
            self.save_search_select_field()
        super(AllinkLegacyChangeAdminForm, self).save(*args, **kwargs)

    def save_search_select_field(self):
        pass
