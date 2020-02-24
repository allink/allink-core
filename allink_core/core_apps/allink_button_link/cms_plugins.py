# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Media, TextInput
from django.contrib.postgres.forms import SplitArrayField
from django.templatetags.static import static
from django.core.exceptions import ValidationError

from djangocms_attributes_field.widgets import AttributesWidget
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from allink_core.core_apps.allink_button_link.models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin
from allink_core.core_apps.allink_button_link import widgets
from allink_core.core.utils import get_additional_choices, update_context_google_tag_manager, get_ratio_choices
from allink_core.core.models.choices import (
    BLANK_CHOICE, NEW_WINDOW, SOFTPAGE,
    FORM_MODAL, IMAGE_MODAL, DEFAULT_MODAL, BUTTON_CONTEXT_CHOICES, CONTEXT_DEFAULT, )
from allink_core.core.forms.fields import SelectLinkField
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin
from allink_core.core.admin.mixins import AllinkMediaAdminMixin


class AllinkButtonLinkContainerPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkButtonLinkContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkButtonLinkContainerPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('BUTTON_LINK_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predifined variations',
                choices=get_additional_choices('BUTTON_LINK_CSS_CLASSES'),
                required=False,
            )


class AllinkButtonLinkPluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):
    LINK_TARGET_REDUCED = (
        (NEW_WINDOW, 'New window'),
        (SOFTPAGE, 'Softpage'),
    )

    link_target_reduced = forms.ChoiceField(label='Link Target', required=False,
                                            choices=BLANK_CHOICE + LINK_TARGET_REDUCED)

    internal_link = SelectLinkField(label='Link Internal', required=False)
    internal_email_addresses = SplitArrayField(forms.EmailField(required=False), size=3, required=False)
    btn_context = forms.ChoiceField(label='Variation', choices=BUTTON_CONTEXT_CHOICES, widget=widgets.Context,
                                    initial=CONTEXT_DEFAULT)

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
            label='Special Links',
            widget=forms.Select(choices=self.instance.get_link_special_choices()),
            required=False,
            help_text=('Important: In case the selected option is a <strong>form</strong>, '
                       'make sure to select <strong>Lightbox (Forms)</strong> '
                       'from the <strong>link target</strong> options for best user experience.'),
        )
        self.fields['ratio'] = forms.CharField(
            label='Ratio',
            help_text='This option overrides the default ratio setting for embeded videos.',
            widget=forms.Select(choices=get_ratio_choices()),
            required=False,
        )
        self.initial['link_target_reduced'] = self.instance.link_target

    def _get_media(self):
        """
        Provide a description of all media required to render the widgets on this form
        """
        media = Media()
        for field in self.fields.values():
            media = media + field.widget.media
        return media + Media(js=['cms/js/libs/jquery.min.js'])

    media = property(_get_media)

    def cleanup_default_link(self, cleaned_data):
        cleaned_data['internal_link'] = None
        cleaned_data['link_page'] = None
        cleaned_data['link_apphook_page'] = None
        cleaned_data['link_object_id'] = None
        cleaned_data['link_model'] = None
        cleaned_data['link_url_name'] = None
        cleaned_data['link_url_kwargs'] = None
        cleaned_data['link_url'] = ''
        cleaned_data['link_anchor'] = ''
        cleaned_data['link_target'] = None
        cleaned_data['link_target_reduced'] = None
        return cleaned_data

    def cleanup_form_link(self, cleaned_data):
        cleaned_data['link_special'] = None
        cleaned_data['send_internal_mail'] = True
        cleaned_data['internal_email_addresses'] = None
        cleaned_data['from_email_address'] = None
        cleaned_data['send_external_mail'] = True
        cleaned_data['thank_you_text'] = None
        cleaned_data['label_layout'] = 'stacked'
        return cleaned_data

    def cleanup_file_link(self, cleaned_data):
        template = cleaned_data.get("template")
        if template != AllinkButtonLinkPlugin.IMAGE_LINK:
            cleaned_data['link_file'] = None
        return cleaned_data

    def cleanup_image_link(self, cleaned_data):
        template = cleaned_data.get("template")
        if template != AllinkButtonLinkPlugin.FILE_LINK:
            cleaned_data['link_file'] = None
        return cleaned_data

    def cleanup_video_embedded_link(self, cleaned_data):
        cleaned_data['video_id'] = None
        cleaned_data['video_service'] = None
        cleaned_data['ratio'] = None
        cleaned_data['auto_start_enabled'] = False
        cleaned_data['allow_fullscreen_enabled'] = True
        return cleaned_data

    def cleanup_video_file_link(self, cleaned_data):
        cleaned_data['video_file'] = None
        cleaned_data['video_poster_image'] = None
        cleaned_data['auto_start_enabled'] = False
        cleaned_data['video_muted_enabled'] = True
        return cleaned_data

    def cleanup_email_link(self, cleaned_data):
        cleaned_data['link_mailto'] = None
        cleaned_data['email_subject'] = None
        cleaned_data['email_body_text'] = None
        return cleaned_data

    def cleanup_phone_link(self, cleaned_data):
        cleaned_data['link_phone'] = None
        return cleaned_data

    def validate_form_link(self, cleaned_data):
        """
        If template is a form which sends emails all the additional fields have to be supplied
        """

        if cleaned_data.get('send_internal_mail') is True:
            # if not cleaned_data.get('from_email_address'):
            #     self.add_error('from_email_address', ValidationError('Please supply an E-Mail Address.'))
            for i in range(3):
                if not cleaned_data.get('internal_email_addresses')[i]:
                    self.add_error(
                        'internal_email_addresses', ValidationError('Please supply at least one E-Mail Address.'))
                    break

        elif cleaned_data.get('send_external_mail') is True:
            if not cleaned_data.get('from_email_address'):
                self.add_error('from_email_address', ValidationError('Please supply an E-Mail Address.'))

    def clean(self):
        cleaned_data = super(AllinkButtonLinkPluginForm, self).clean()
        template = cleaned_data.get("template")
        old_template = self.initial.get('template')

        cleanup_template_mapper = {
            AllinkButtonLinkPlugin.DEFAULT_LINK: self.cleanup_default_link,
            AllinkButtonLinkPlugin.FORM_LINK: self.cleanup_form_link,
            AllinkButtonLinkPlugin.FILE_LINK: self.cleanup_file_link,
            AllinkButtonLinkPlugin.IMAGE_LINK: self.cleanup_image_link,
            AllinkButtonLinkPlugin.VIDEO_EMBEDDED_LINK: self.cleanup_video_embedded_link,
            AllinkButtonLinkPlugin.VIDEO_FILE_LINK: self.cleanup_video_file_link,
            AllinkButtonLinkPlugin.EMAIL_LINK: self.cleanup_email_link,
            AllinkButtonLinkPlugin.PHONE_LINK: self.cleanup_phone_link,
        }

        # validation_mapper = {
        #     AllinkButtonLinkPlugin.FORM_LINK: self.validate_form_link,
        # }

        link_target_mapper = {
            # double check for empty string
            AllinkButtonLinkPlugin.DEFAULT_LINK: cleaned_data.get('link_target_reduced', None) or None,
            AllinkButtonLinkPlugin.FORM_LINK: FORM_MODAL,
            AllinkButtonLinkPlugin.FILE_LINK: NEW_WINDOW,
            AllinkButtonLinkPlugin.IMAGE_LINK: IMAGE_MODAL,
            AllinkButtonLinkPlugin.VIDEO_EMBEDDED_LINK: DEFAULT_MODAL,
            AllinkButtonLinkPlugin.VIDEO_FILE_LINK: DEFAULT_MODAL,
        }

        # if template has changed, delete all obsolete fields
        if old_template and template != old_template:
            cleanup_template_mapper.get(old_template)(cleaned_data)

        # validate different link types
        # validation_mapper.get(template)()

        # TODO we make this nicer when we add tests

        # always open external_links in new tab
        if cleaned_data['link_url']:
            cleaned_data['link_target'] = NEW_WINDOW

        cleaned_data['link_target'] = link_target_mapper.get(template)

        return cleaned_data


@plugin_pool.register_plugin
class CMSAllinkButtonLinkContainerPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkButtonLinkContainerPlugin
    name = 'Button/ Link Container'
    module = 'Generic'
    allow_children = True
    child_classes = ['CMSAllinkButtonLinkPlugin']
    form = AllinkButtonLinkContainerPluginForm

    fieldsets = (
        (None, {
            'fields': (
                'alignment_horizontal_desktop',
                'alignment_horizontal_mobile',
            ),
        }),
        ('Advanced settings', {
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
class CMSAllinkButtonLinkPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkButtonLinkPlugin
    name = 'Button/ Link'
    module = 'Generic'
    allow_children = False
    form = AllinkButtonLinkPluginForm
    change_form_template = 'admin/allink_button_link/change_form.html'
    render_template = 'allink_button_link/item.html'
    text_enabled = True

    fieldsets = (
        (None, {
            'fields': (
                'template',
                'label',
            ),
        }),
        ('Link style', {
            'classes': (
                'collapse',
            ),
            'fields': (
                'type',
                'btn_context',
                'btn_size',
            )
        }),
        ('Internal/External link settings', {
            'classes': (
                'only_when_default_link',
            ),
            'fields': (
                'internal_link',
                'link_url',
                'link_anchor',
                'link_target_reduced',
            )
        }),
        ('File link settings', {
            'classes': (
                'only_when_file_link',
                'only_when_image_link',
            ),
            'fields': (
                'link_file',
            )
        }),
        ('Phone link settings', {
            'classes': (
                'only_when_phone_link',
            ),
            'fields': (
                'link_phone',
            )
        }),
        ('Email link settings', {
            'classes': (
                'only_when_email_link',
            ),
            'fields': (
                'link_mailto',
                'email_subject',
                'email_body_text',
            )
        }),
        ('Form link settings', {
            'classes': (
                'only_when_form_link',
            ),
            'fields': (
                'link_special',
                'send_internal_mail',
                'internal_email_addresses',
                'from_email_address',
                'send_external_mail',
                'thank_you_text',
                'label_layout',
            )
        }),
        ('Video (Embedded) link settings', {
            'classes': (
                'only_when_video_embedded_link',
            ),
            'fields': (
                'video_id',
                'video_service',
                'ratio',
                'auto_start_enabled',
                'allow_fullscreen_enabled',
            )
        }),
        ('Video (File) link settings', {
            'classes': (
                'only_when_video_file_link',
            ),
            'fields': (
                'video_file',
                'video_poster_image',
                'auto_start_enabled',
                'video_muted_enabled',
            )
        }),
        ('Modal Closing options', {
            'classes': (
                'collapse',
                'only_when_image_link',
                'only_when_form_link',
                'only_when_video_embedded_link',
                'only_when_video_file_link',
            ),
            'fields': (
                'data_modal_escape_close_enabled',
                'data_modal_overlay_close_enabled',
                'data_modal_button_close_enabled',
            )
        }),
        ('Advanced settings', {
            'classes': ('collapse',),
            'fields': (
                'link_attributes',
            )
        }),
        ('Hidden settings', {
            'classes': ('hidden',),
            'fields': (
                'link_target',
            )
        }),
    )

    @classmethod
    def get_render_queryset(cls):
        return cls.model._default_manager.all()

    def icon_src(self, instance):
        return static('aldryn_bootstrap3/img/type/button.png')

    def get_render_template(self, context, instance, placeholder):

        template = 'allink_button_link/item.html'
        return template

    def render(self, context, instance, placeholder):
        context = super(CMSAllinkButtonLinkPlugin, self).render(context, instance, placeholder)

        # set svg icons
        if instance.softpage_enabled:
            context.update({'icon': 'softpage'})
        if instance.new_window_enabled:
            context.update({'icon': 'arrow-external'})

        if instance.page:
            context = update_context_google_tag_manager(
                page_name=instance.page.__str__(),
                page_id=instance.page.id,
                plugin_id=instance.id,
                name=instance.label,
                context=context
            )
        else:
            try:
                context = update_context_google_tag_manager(
                    page_name=instance.placeholder.slot,
                    page_id=instance.placeholder.id,
                    plugin_id=instance.id,
                    name=instance.label,
                    context=context
                )
            except AttributeError:
                context = update_context_google_tag_manager(
                    plugin_id=instance.id,
                    name=instance.label,
                    context=context
                )
        return context
