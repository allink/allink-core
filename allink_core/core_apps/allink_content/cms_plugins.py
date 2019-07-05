# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from allink_core.core.utils import get_additional_choices
from allink_core.core.forms.fields import ColorField
from allink_core.core_apps.allink_content.models import AllinkContentPlugin, AllinkContentColumnPlugin


class AllinkContentPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkContentPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkContentPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label=_('Template'),
            widget=forms.Select(choices=self.instance.get_template_choices()),
            required=True,
        )
        if get_additional_choices('CONTENT_TITLE_CHOICES'):
            self.fields['title_size'] = forms.CharField(
                label=_('Section Title Size'),
                widget=forms.Select(
                    choices=get_additional_choices('CONTENT_TITLE_CHOICES'),
                ),
                initial=settings.CONTENT_TITLE_CHOICES_DEFAULT,
                required=False,
            )
        else:
            self.fields['title_size'] = forms.CharField(widget=forms.HiddenInput(), required=False)

        self.fields['bg_color'] = ColorField(
            label=_('Background color'),
            required=False,
        )

        if get_additional_choices('CONTENT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_('Predifined variations'),
                choices=get_additional_choices('CONTENT_CSS_CLASSES'),
                required=False,
            )
        if get_additional_choices('CONTENT_ON_SCREEN_EFFECT_CHOICES'):
            self.fields['project_on_screen_effect'] = forms.ChoiceField(
                label=_('Predifined on screen Effect'),
                choices=get_additional_choices('CONTENT_ON_SCREEN_EFFECT_CHOICES', blank=True),
                initial='default',
                required=False,
            )
        if get_additional_choices('CONTENT_SPACINGS'):
            self.fields['project_css_spacings_top_bottom'] = forms.ChoiceField(
                label=_('Spacings top & bottom'),
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )
        if get_additional_choices('CONTENT_SPACINGS'):
            self.fields['project_css_spacings_top'] = forms.ChoiceField(
                label=_('Spacings top'),
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )
        if get_additional_choices('CONTENT_SPACINGS'):
            self.fields['project_css_spacings_bottom'] = forms.ChoiceField(
                label=_('Spacings bottom'),
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )

    def clean(self):
        cleaned_data = super(AllinkContentPluginForm, self).clean()
        if self.instance.pk:
            # if column count is not the same, dont allow template to change
            if self.instance.get_template_column_count(self.instance.template) != self.instance.get_template_column_count(cleaned_data['template']):  # noqa
                self.add_error('template', _('You can only change the template if it'
                                             ' has the same amount of columns as the previous template.'))
        return cleaned_data


class AllinkContentColumnPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkContentColumnPlugin
        exclude = ('title', 'page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkContentColumnPluginForm, self).__init__(*args, **kwargs)
        parent_column_amount = AllinkContentPlugin.get_template_column_count(kwargs.get('instance').template)
        self.fields['order_mobile'].widget = forms.Select(choices=enumerate(range(1, parent_column_amount + 1)))


@plugin_pool.register_plugin
class CMSAllinkContentPlugin(CMSPluginBase):
    model = AllinkContentPlugin
    name = _('Content')
    module = _('Generic')
    render_template = "allink_content/default/content.html"
    allow_children = True
    child_classes = ['ContentColumnPlugin']
    form = AllinkContentPluginForm

    class Media:
        js = (get_files('djangocms_custom_admin')[1]['publicPath'],)
        css = {
            'all': (get_files('djangocms_custom_admin')[0]['publicPath'],)
        }

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'title_size',
                'template',
            ),
        }),
        (_('Section Options'), {
            'classes': ('collapse',),
            'fields': [
                'container_enabled',
                'inverted_colors_enabled',
                'overlay_enabled',
                'bg_color',
            ]
        }),
        (_('Spacings'), {
            'classes': ('collapse',),
            'fields': [
                'project_css_spacings_top_bottom',
                'project_css_spacings_top',
                'project_css_spacings_bottom',
            ]
        }),
        (_('Background Image (full width)'), {
            'classes': ('collapse',),
            'fields': (
                'bg_image_outer_container',
                'dynamic_height_enabled',
            )
        }),
        (_('Background Video (Important: Only works if all fields are set)'), {
            'classes': ('collapse',),
            'fields': (
                'video_file',
                'video_poster_image',
                'video_mobile_image',
            )
        }),
        (_('Advanced Options'), {
            'classes': ('collapse',),
            'fields': (
                'project_css_classes',
                'project_on_screen_effect',
                'anchor',
                'ignore_in_pdf',
            )
        })
    )

    @classmethod
    def get_render_queryset(cls):
        return cls.model._default_manager.all()

    def save_model(self, request, obj, form, change):
        response = super(CMSAllinkContentPlugin, self).save_model(request, obj, form, change)
        if obj.numchild == 0:
            column_amount = AllinkContentPlugin.get_template_column_count(form.cleaned_data['template'])

            for x in range(int(column_amount)):
                col = AllinkContentColumnPlugin(
                    parent=obj,
                    placeholder=obj.placeholder,
                    language=obj.language,
                    position=CMSPlugin.objects.filter(parent=obj).count(),
                    plugin_type=CMSAllinkContentColumnPlugin.__name__
                )
                col.save()
        return response

    def render(self, context, instance, placeholder):
        # disable onscreen effect when edit mode is active
        if context['request'].toolbar and context['request'].toolbar.edit_mode_active:
            instance.project_on_screen_effect = False
        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class CMSAllinkContentColumnPlugin(CMSPluginBase):
    model = AllinkContentColumnPlugin
    name = _("Column")
    module = _('Generic')
    render_template = "allink_content/default/column.html"
    parent_classes = ["AllinkContentPlugin"]
    allow_children = True
    child_classes = settings.ALLINK_CONTENT_PLUGIN_CHILD_CLASSES
    form = AllinkContentColumnPluginForm
    require_parent = True

    disable_copyable_menu = True
    disable_cutable_menu = True
    disable_deletable_menu = True

    class Media:
        js = (get_files('djangocms_custom_admin')[1]['publicPath'],)
        css = {
            'all': (get_files('djangocms_custom_admin')[0]['publicPath'],)
        }

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):

        if 'order_mobile' in form.changed_data:
            parent = obj.parent.get_plugin_instance()[0]
            for column in parent.get_children():
                if column.plugin_type == 'CMSAllinkContentColumnPlugin':
                    #  change the column which had the same ordering before
                    #  to the value which our changed column had before
                    child_column = column.get_plugin_instance()[0]
                    if child_column.order_mobile == form.cleaned_data.get('order_mobile'):
                        child_column.order_mobile = form.initial.get('order_mobile')
                        child_column.save()
        return super(CMSAllinkContentColumnPlugin, self).save_model(request, obj, form, change)
