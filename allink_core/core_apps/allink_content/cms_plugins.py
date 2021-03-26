# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from allink_core.core.utils import get_additional_choices
from allink_core.core.forms.fields import ColorField
from allink_core.core_apps.allink_content.models import AllinkContentPlugin, AllinkContentColumnPlugin
from allink_core.core.admin.mixins import AllinkMediaAdminMixin


class AllinkContentPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkContentPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkContentPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label='Template',
            widget=forms.Select(choices=self.instance.get_template_choices()),
            required=True,
        )
        if get_additional_choices('CONTENT_TITLE_CHOICES'):
            self.fields['title_size'] = forms.CharField(
                label='Section Title Size',
                widget=forms.Select(
                    choices=get_additional_choices('CONTENT_TITLE_CHOICES'),
                ),
                initial=settings.CONTENT_TITLE_CHOICES_DEFAULT,
                required=False,
            )
        else:
            self.fields['title_size'] = forms.CharField(widget=forms.HiddenInput(), required=False)

        self.fields['bg_color'] = ColorField(
            label='Background color',
            required=False,
        )

        if get_additional_choices('CONTENT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predifined variations',
                choices=get_additional_choices('CONTENT_CSS_CLASSES'),
                initial=get_additional_choices('INITIAL_CONTENT_CSS_CLASSES'),
                required=False,
            )
        if get_additional_choices('CONTENT_SPACINGS'):
            self.fields['project_css_spacings_top_bottom'] = forms.ChoiceField(
                label='Spacings top & bottom',
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )
        if get_additional_choices('CONTENT_SPACINGS'):
            self.fields['project_css_spacings_top'] = forms.ChoiceField(
                label='Spacings top',
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )
        if get_additional_choices('CONTENT_SPACINGS'):
            self.fields['project_css_spacings_bottom'] = forms.ChoiceField(
                label='Spacings bottom',
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )

    def clean(self):
        cleaned_data = super(AllinkContentPluginForm, self).clean()
        if self.instance.pk:
            # if column count is not the same, dont allow template to change
            if self.instance.get_template_column_count(
                    self.instance.template) != self.instance.get_template_column_count(
                cleaned_data['template']):  # noqa
                self.add_error('template', 'You can only change the template if it'
                                           ' has the same amount of columns as the previous template.')
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
class CMSAllinkContentPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkContentPlugin
    name = 'Content'
    module = 'Generic'
    render_template = "allink_content/default/content.html"
    allow_children = True
    child_classes = ['ContentColumnPlugin']
    form = AllinkContentPluginForm

    def get_fieldsets(self, request, obj=None):
        """
        CONTENT_EXTENDED_FEATURE_SET = False will remove the following fields:
        'bg_image_outer_container', 'video_file', 'video_poster_image', 'video_mobile_image'
        """

        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'title_size',
                    'template',
                ),
            }),
            ('Section Options', {
                'classes': ('collapse',),
                'fields': [
                    'container_enabled',
                    'inverted_colors_enabled',
                    'overlay_enabled',
                    'bg_color',
                ]
            }),
            ('Spacings', {
                'classes': ('collapse',),
                'fields': [
                    'project_css_spacings_top_bottom',
                    'project_css_spacings_top',
                    'project_css_spacings_bottom',
                ]
            })
        )
        
        if getattr(settings, 'CONTENT_EXTENDED_FEATURE_SET', True):
            fieldsets += (
                ('Background Image (full width)', {
                    'classes': ('collapse',),
                    'fields': (
                        'bg_image_outer_container',
                        'dynamic_height_enabled',
                    )
                }),
                ('Background Video (Important: Only works if all fields are set)', {
                    'classes': ('collapse',),
                    'fields': (
                        'video_file',
                        'video_poster_image',
                        'video_mobile_image',
                    )
                })
            )

        fieldsets += (('Advanced Options', {
            'classes': ('collapse',),
            'fields': (
                'project_css_classes',
                'anchor',
                'ignore_in_pdf',
            )
        })),
        return fieldsets

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
                    order_mobile=CMSPlugin.objects.filter(parent=obj).count(),
                    plugin_type=CMSAllinkContentColumnPlugin.__name__
                )
                col.save()
        return response


def render(self, context, instance, placeholder):
    return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class CMSAllinkContentColumnPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkContentColumnPlugin
    name = "Column"
    module = 'Generic'
    render_template = "allink_content/default/column.html"
    parent_classes = ["AllinkContentPlugin"]
    allow_children = True
    child_classes = settings.ALLINK_CONTENT_PLUGIN_CHILD_CLASSES
    form = AllinkContentColumnPluginForm
    require_parent = True

    disable_copyable_menu = True
    disable_cutable_menu = True
    disable_deletable_menu = True

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
