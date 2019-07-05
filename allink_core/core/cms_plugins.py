# -*- coding: utf-8 -*-
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.admin.widgets import FilteredSelectMultiple

from cms.plugin_base import CMSPluginBase
from webpack_loader.utils import get_files

from allink_core.core.models import AllinkBaseAppContentPlugin, AllinkBaseSearchPlugin
from allink_core.core.utils import get_project_css_classes


class AllinkBaseAppContentPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkBaseAppContentPlugin
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(AllinkBaseAppContentPluginForm, self).__init__(*args, **kwargs)
        # if app uses categories, populate 'categories' field
        if self.instance.get_app_can_have_categories():
            self.fields['categories'] = forms.ModelMultipleChoiceField(
                label=_('Categories'),
                widget=FilteredSelectMultiple(
                    verbose_name=_('Categories'),
                    is_stacked=True
                ),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
            self.fields['categories_and'] = forms.ModelMultipleChoiceField(
                label=_('Categories (AND operator)'),
                widget=FilteredSelectMultiple(
                    verbose_name=_('Categories'),
                    is_stacked=True
                ),
                help_text=_(
                    u'Use this field if you want to further restrict your result set. This option allows you to create'
                    u' a conjunction between the first set of categories in field "Categories" and the ones '
                    u'specified here.'),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
            self.fields['category_navigation'] = forms.ModelMultipleChoiceField(
                label=_('Categories for Navigation'),
                widget=FilteredSelectMultiple(
                    verbose_name=_('Categories for Navigation'),
                    is_stacked=True
                ),
                help_text=_(
                    u'You can explicitly define the categories for the category navigation here. '
                    u'This will override the'
                    u' automatically set of categories. (From "Filter & Ordering" but not from the "Manual entries")'),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
        self.fields['filter_fields'] = forms.TypedMultipleChoiceField(
            label=_('Filter Fields'),
            help_text=_('A Select Dropdown will be displayed for this Fields.'),
            choices=((field[0], field[1]['verbose']) for field in self.instance.FILTER_FIELD_CHOICES),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        self.fields['template'] = forms.CharField(
            label=_('Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
        if get_project_css_classes(self._meta.model.data_model._meta.model_name):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_('Predifined variations'),
                choices=get_project_css_classes(self._meta.model.data_model._meta.model_name),
                required=False,
            )
        self.fields['manual_filtering'] = forms.CharField(
            label=_('Filtering'),
            required=False,
            widget=forms.Select(choices=self.instance.get_filtering_choices() if hasattr(
                self.instance, 'get_filtering_choices') else [])
        )
        self.fields['manual_ordering'] = forms.CharField(
            label=_('Ordering'),
            required=False,
            widget=forms.Select(choices=self.instance.get_ordering_choices())
        )


class CMSAllinkBaseAppContentPlugin(CMSPluginBase):
    """
    is not registered itself
    only used to inherit from (for specific App Content Plugins)
    """
    model = AllinkBaseAppContentPlugin

    name = _('App Content')
    module = _('allink modules')
    allow_children = False
    form = AllinkBaseAppContentPluginForm

    class Media:
        js = (get_files('djangocms_custom_admin')[1]['publicPath'],)
        css = {
            'all': (get_files('djangocms_custom_admin')[0]['publicPath'],)
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': [
                    'template',
                ],
            }),
        )

        fieldsets += (_('Display Options'), {
            'classes': ('collapse',),
            'fields': (
                'detail_link_enabled',
                'softpage_enabled',
            )
        }),

        if self.model.data_model.get_can_have_categories():
            fieldsets += (_('Categories'), {
                'classes': ('collapse',),
                'fields': (
                    'categories',
                    'categories_and',
                )
            }),

        fieldsets += (_('Filter & Ordering'), {
            'classes': ('collapse',),
            'fields': (
                'manual_filtering',
                'manual_ordering',
                'filter_fields',
            )
        }),

        fieldsets += (_('Select entries manually'), {
            'classes': ('collapse',),
            'fields': (
                'manual_entries',
            )
        }),

        if self.model.data_model.get_can_have_categories():
            fieldsets += (_('Category Navigation Options'), {
                'classes': (
                    'collapse',
                    'disable_when_slider',
                    'disable_when_map',
                ),
                'fields': (
                    'category_navigation_enabled',
                    'category_navigation_all',
                    'category_navigation',
                )
            }),

        fieldsets += (_('Number of entries'), {
            'classes': (
                'collapse',
                'disable_when_map',
            ),
            'fields': (
                ('paginated_by',),
            )
        }),

        fieldsets += (_('Pagination Options'), {
            'classes': (
                'collapse',
                'disable_when_slider',
                'disable_when_map',
            ),
            'fields': (
                ('pagination_type', 'load_more_button_text'),
            )
        }),

        fieldsets += (_('Additional Options'), {
            'classes': ('collapse',),
            'fields': (
                'apphook_page',
                'detail_link_text',
                'project_css_classes',
            )
        }),

        fieldsets += (_('Grid Options'), {
            'classes': (
                'collapse',
                'only_when_grid_static',
                'only_when_grid_dynamic',
            ),
            'fields': (
                'items_per_row',
            )
        }),

        return fieldsets

    def get_application_namespace(self, instance):
        if getattr(instance, 'apphook_page'):
            return instance.apphook_page.application_namespace
        else:
            return self.model.data_model._meta.model_name

    def get_render_template(self, context, instance, placeholder):
        file = 'no_results' if not context['object_list'] else 'content'
        return instance.get_correct_template(file)

    def get_queryset_by_category(self, instance, filters, request):
        # manual entries
        if instance.fetch_manual_entries:  # TODO unnecessary query? split up into two different Plugins?
            object_list = instance.get_selected_entries(filters=filters)
        # category navigation and no category "all" (only first category is relevant)
        elif instance.category_navigation_enabled and not instance.category_navigation_all:
            object_list = instance.get_render_queryset_for_display(
                category=instance.fetch_first_category, filters=filters, request=request)
        else:
            object_list = instance.get_render_queryset_for_display(filters=filters, request=request)
        return object_list

    def render(self, context, instance, placeholder):
        # getting filter parameters and attributes
        filters = {re.sub('filter-%s-' % instance.data_model._meta.model_name, '', k):
                   v for k, v in context['request'].GET.items()
                   if (k.startswith('filter-%s-' % instance.data_model._meta.model_name) and v != 'None')}

        # random ordering needs sessioncaching for object_list
        if instance.manual_ordering == AllinkBaseAppContentPlugin.RANDOM:
            object_list, path = context['request'].session.get("random_plugin_queryset_%s" % instance.id, ([], None))
            if (object_list and path == context['request'].path) or not object_list:
                object_list = self.get_queryset_by_category(instance, filters, context['request'])
                context['request'].session["random_plugin_queryset_%s" % instance.id] = (object_list,
                                                                                         context['request'].path)

        # not random ordering
        else:
            object_list = self.get_queryset_by_category(instance, filters, context['request'])

        # Paginate Objects
        if instance.paginated_by > 0:
            paginator = Paginator(object_list, instance.paginated_by)
            firstpage = paginator.page(1)
            object_list = firstpage.object_list

            # Load More
            if (
                instance.pagination_type == AllinkBaseAppContentPlugin.LOAD
                    or instance.pagination_type == AllinkBaseAppContentPlugin.LOAD_REST) and firstpage.has_next():
                context['page_obj'] = firstpage
                context.update(
                    {'next_page_url': reverse('{}:more'.format(self.get_application_namespace(instance)),
                                              kwargs={
                                                  'page': context['page_obj'].next_page_number()}) + '?api_request=1'
                        + '&plugin_id={}'.format(instance.id)})

                if instance.category_navigation_enabled and not instance.category_navigation_all:
                    context['next_page_url'] = context['next_page_url'] + '&category={}'.format(
                        instance.fetch_first_category.id)

        # category navigation
        if instance.category_navigation_enabled or instance.filter_fields:
            context.update(
                {'by_category': reverse('{}:more'.format(self.get_application_namespace(instance)),
                                        kwargs={'page': 1}) + '?api_request=1' + '&plugin_id={}'.format(instance.id)})

        context['instance'] = instance
        context['placeholder'] = placeholder
        context['object_list'] = object_list

        if instance.category_navigation_enabled:
            context['category_navigation'] = instance.fetch_category_navigation

        return context


class AllinkBaseSearchPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkBaseAppContentPlugin
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(AllinkBaseSearchPluginForm, self).__init__(*args, **kwargs)
        if get_project_css_classes(self._meta.model.data_model._meta.model_name):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_('Predifined variations'),
                choices=get_project_css_classes(self._meta.model.data_model._meta.model_name),
                required=False,
            )

        self.fields['template'] = forms.CharField(
            label=_('Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )


class CMSAllinkBaseSearchPlugin(CMSPluginBase):
    """
    is not registered itself
    only used to inherit from (for specific Search Plugins)
    """
    model = AllinkBaseSearchPlugin
    module = _('allink search')
    form = AllinkBaseSearchPluginForm
    search_form = None

    class Media:
        js = (get_files('djangocms_custom_admin')[1]['publicPath'],)
        css = {
            'all': (get_files('djangocms_custom_admin')[0]['publicPath'],)
        }

    def get_render_template(self, context, instance, placeholder):
        return '{}/plugins/{}/content.html'.format(self.model.data_model._meta.app_label, instance.template)

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder

        form = self.search_form()
        object_list = self.model.data_model.objects.active()

        additional_context = [
            ('form', form),
            ('object_list', object_list),
        ]

        for key, val in additional_context:
            context.update({key: val})

        return context

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': [
                    'project_css_classes',
                    'template'
                ],
            }),
        )
        return fieldsets
