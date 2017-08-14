# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Media, TextInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.forms import SplitArrayField
from django.templatetags.static import static

from djangocms_attributes_field.widgets import AttributesWidget
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from allink_core.core_apps.allink_button_link.models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin
from allink_core.core.utils import get_additional_choices
from allink_core.core.forms.fields import SelectLinkField
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin


class AllinkButtonLinkContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkButtonLinkContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkButtonLinkContainerPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('BUTTON_LINK_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations'),
                choices=get_additional_choices('BUTTON_LINK_CSS_CLASSES'),
                required=False,
            )


class AllinkButtonLinkPluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):

    internal_link = SelectLinkField(label=_('Link Internal'), required=False)
    internal_email_addresses = SplitArrayField(forms.EmailField(required=False), size=3, required=False)

    class Meta:
        model = AllinkButtonLinkPlugin
        exclude = (
            'page', 'position', 'placeholder', 'language', 'plugin_type',
        )
        # When used inside djangocms-text-ckeditor
        # this causes the label field to be prefilled with the selected text.
        widgets = {
            'label': TextInput(attrs={'class': 'js-ckeditor-use-selected-text'}),
        }

    def __init__(self, *args, **kwargs):
        super(AllinkButtonLinkPluginForm, self).__init__(*args, **kwargs)
        self.fields['link_attributes'].widget = AttributesWidget()
        self.fields['link_special'] = forms.CharField(
            label=_(u'Special Links'),
            widget=forms.Select(choices=self.instance.get_link_special_choices()),
            required=False,
            help_text=_(u'Important: In case the selected option is a <strong>form</strong>, make sure to select <strong>Lightbox (Forms)</strong> from the <strong>link target</strong> options for best user experience.'),
        )

    def _get_media(self):
        """
        Provide a description of all media required to render the widgets on this form
        """
        media = Media()
        for field in self.fields.values():
            media = media + field.widget.media
        media._js = ['cms/js/libs/jquery.min.js'] + media._js
        return media
    media = property(_get_media)

    def clean(self):
        from django.core.exceptions import ValidationError
        # If special_link is a form which sends emails all the additional fields have to be supplied
        self.cleaned_data = super(AllinkButtonLinkPluginForm, self).clean()
        if ':request' in self.cleaned_data.get('link_special') and \
            (self.cleaned_data.get('send_internal_mail') == True
             and not self.cleaned_data.get('internal_email_addresses')[0]
             and not self.cleaned_data.get('internal_email_addresses')[1]
             and not self.cleaned_data.get('internal_email_addresses')[2]):
            self.add_error('internal_email_addresses', ValidationError(_(u'Please supply at least one E-Mail Address.')))
        if ':request' in self.cleaned_data.get('link_special') and (self.cleaned_data.get('send_external_mail') == True and not self.cleaned_data.get('from_email_address')):
            self.add_error('from_email_address', ValidationError(_(u'Please supply an E-Mail Address.')))
        return self.cleaned_data


@plugin_pool.register_plugin
class CMSAllinkButtonLinkContainerPlugin(CMSPluginBase):
    model = AllinkButtonLinkContainerPlugin
    name = _('Button/ Link Container')
    module = _('Generic')
    allow_children = True
    child_classes = ['CMSAllinkButtonLinkPlugin']
    form = AllinkButtonLinkContainerPluginForm
    cache = False

    class Media:
        js = (
            get_files('djangocms_custom_admin')[0]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[1]['publicPath'],

            )
        }

    fieldsets = (
        (None, {
            'fields': (
                'alignment_horizontal_desktop',
                'alignment_horizontal_mobile',
            ),
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'project_css_classes',
            )
        }),
    )

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_button_link/content.html'
        return template


@plugin_pool.register_plugin
class CMSAllinkButtonLinkPlugin(CMSPluginBase):
    model = AllinkButtonLinkPlugin
    name = _('Button/ Link')
    module = _('Generic')
    allow_children = False
    form = AllinkButtonLinkPluginForm
    change_form_template = 'admin/allink_button_link/change_form.html'
    render_template = 'allink_button_link/item.html'
    text_enabled = True
    cache = False

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    fieldsets = (
        (None, {
            'fields': (
                'label',
                'type',
                'btn_context',
                # 'txt_context',
                'btn_size',
                # ('icon_left', 'icon_right', 'btn_block',),
            ),
        }),
        (_('Link settings'), {
            # 'classes': ('collapse',),
            'fields': (
                'internal_link',
                'link_url',
                ('link_mailto', 'link_phone'),
                ('link_anchor', 'link_special'),
                'link_file',
                'link_target',
            )
        }),
        (_('Additional email settings'), {
            'classes': ('collapse',),
            'fields': (
                'email_subject',
                'email_body_text',
            )
        }),
        (_('Additional form settings'), {
            'classes': ('collapse',),
            'fields': (
                'send_internal_mail',
                'internal_email_addresses',
                'from_email_address',
                'send_external_mail',
                'thank_you_text',
                'label_layout',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'link_attributes',
            )
        }),
    )

    def icon_src(self, instance):
        return static('aldryn_bootstrap3/img/type/button.png')

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_button_link/item.html'
        return template

    def render(self, context, instance, placeholder):
        context = super(CMSAllinkButtonLinkPlugin, self).render(context, instance, placeholder)
        return context
