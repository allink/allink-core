# -*- coding: utf-8 -*-
from django import forms
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.admin.widgets import FilteredSelectMultiple

from cms.plugin_base import CMSPluginBase

from allink_core.core.models import AllinkBaseAppContentPlugin, AllinkBaseSearchPlugin, AllinkBaseSectionPlugin
from allink_core.core.utils import get_project_css_classes, get_additional_choices
from allink_core.core.admin.mixins import AllinkMediaAdminMixin


class AllinkBaseAppContentPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkBaseAppContentPlugin
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(AllinkBaseAppContentPluginForm, self).__init__(*args, **kwargs)
        # if app uses categories, populate 'categories' field
        if self.instance.get_app_can_have_categories():
            self.fields['categories'] = forms.ModelMultipleChoiceField(
                label='Categories',
                widget=FilteredSelectMultiple(
                    verbose_name='Categories',
                    is_stacked=True
                ),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
            self.fields['categories_and'] = forms.ModelMultipleChoiceField(
                label='Categories (AND operator)',
                widget=FilteredSelectMultiple(
                    verbose_name='Categories',
                    is_stacked=True
                ),
                help_text=(
                    'Use this field if you want to further restrict your result set. This option allows you to create'
                    ' a conjunction between the first set of categories in field "Categories" and the ones '
                    'specified here.'),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
            self.fields['category_navigation'] = forms.ModelMultipleChoiceField(
                label='Categories for Navigation',
                widget=FilteredSelectMultiple(
                    verbose_name='Categories for Navigation',
                    is_stacked=True
                ),
                help_text=(
                    'You can explicitly define the categories for the category navigation here. '
                    'This will override the'
                    ' automatically set of categories. (From "Filter & Ordering" but not from the "Manual entries")'),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )

        self.fields['template'] = forms.CharField(
            label='Template',
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
        if get_project_css_classes(self._meta.model.data_model._meta.model_name):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predifined variations',
                choices=get_project_css_classes(self._meta.model.data_model._meta.model_name),
                required=False,
            )
        self.fields['manual_filtering'] = forms.CharField(
            label='Filtering',
            required=False,
            widget=forms.Select(choices=self.instance.get_filtering_choices() if hasattr(
                self.instance, 'get_filtering_choices') else [])
        )
        self.fields['manual_ordering'] = forms.CharField(
            label='Ordering',
            required=False,
            widget=forms.Select(choices=self.instance.get_ordering_choices())
        )


class CMSAllinkBaseAppContentPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    """
    is not registered itself
    only used to inherit from (for specific App Content Plugins)
    """
    model = AllinkBaseAppContentPlugin

    name = 'App Content'
    module = 'allink modules'
    allow_children = False
    form = AllinkBaseAppContentPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': [
                    'template',
                ],
            }),
        )

        fieldsets += ('Display Options', {
            'classes': ('collapse',),
            'fields': (
                'detail_link_enabled',
                'softpage_enabled',
            )
        }),

        if self.model.data_model.get_can_have_categories():
            fieldsets += ('Categories', {
                'classes': ('collapse',),
                'fields': (
                    'categories',
                    'categories_and',
                )
            }),

        fieldsets += ('Filter & Ordering', {
            'classes': ('collapse',),
            'fields': (
                'manual_filtering',
                'manual_ordering',
            )
        }),

        fieldsets += ('Select entries manually', {
            'classes': ('collapse',),
            'fields': (
                'manual_entries',
            )
        }),

        if self.model.data_model.get_can_have_categories():
            fieldsets += ('Category Navigation Options', {
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

        fieldsets += ('Number of entries', {
            'classes': (
                'collapse',
                'disable_when_map',
            ),
            'fields': (
                ('paginated_by',),
            )
        }),

        fieldsets += ('Pagination Options', {
            'classes': (
                'collapse',
                'disable_when_slider',
                'disable_when_map',
            ),
            'fields': (
                ('pagination_type', 'load_more_button_text'),
                'load_more_internallink',
            )
        }),

        fieldsets += ('Additional Options', {
            'classes': ('collapse',),
            'fields': (
                'apphook_page',
                'detail_link_text',
                'project_css_classes',
            )
        }),

        fieldsets += ('Grid Options', {
            'classes': (
                'collapse',
                'only_when_grid_static',
                'only_when_grid_static_newsletter',
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

    def get_queryset_by_category(self, instance):
        # category navigation and no category "all" (only first category is relevant)
        if instance.category_navigation_enabled and not instance.category_navigation_all:
            object_list = instance.get_render_queryset_for_display(category=instance.fetch_first_category)
        else:
            object_list = instance.get_render_queryset_for_display()
        return object_list

    def render(self, context, instance, placeholder):

        object_list = self.get_queryset_by_category(instance)

        # Paginate Objects
        if instance.paginated_by > 0:
            paginator = Paginator(object_list, instance.paginated_by)
            firstpage = paginator.page(1)
            object_list = firstpage.object_list

            # Load More
            if (instance.pagination_type == AllinkBaseAppContentPlugin.LOAD
                or instance.pagination_type == AllinkBaseAppContentPlugin.LOAD_REST) \
                    and firstpage.has_next():
                context['page_obj'] = firstpage
                context.update(
                    {'next_page_url': reverse('{}:more'.format(
                        self.get_application_namespace(instance)), kwargs={
                        'page': context['page_obj'].next_page_number()}) + '?plugin_id={}'.format(instance.id)})

                if instance.category_navigation_enabled and not instance.category_navigation_all:
                    context['next_page_url'] = \
                        context['next_page_url'] + '&category={}'.format(instance.fetch_category_navigation[0].id)

        # category navigation
        if instance.category_navigation_enabled:
            context.update(
                {'by_category': reverse('{}:more'.format(self.get_application_namespace(instance)),
                                        kwargs={'page': 1}) + '?plugin_id={}'.format(instance.id)})

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
                label='Predifined variations',
                choices=get_project_css_classes(self._meta.model.data_model._meta.model_name),
                required=False,
            )

        self.fields['template'] = forms.CharField(
            label='Template',
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )


class CMSAllinkBaseSearchPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    """
    is not registered itself
    only used to inherit from (for specific Search Plugins)
    """
    model = AllinkBaseSearchPlugin
    module = 'allink search'
    form = AllinkBaseSearchPluginForm
    search_form = None

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


class CMSAllinkBaseFormPlugin(CMSPluginBase):
    """
    Use this BasePlugin for plugins, which display a form.

    example implementation:

    class CMSLivingSignupPlugin(CMSAllinkBaseFormPlugin):
        name = 'Living Signup Plugin'
        model = LivingSignupPlugin
        render_template = 'living/plugins/signup/content.html'

        form_class = LivingSignupForm
        url_name = 'signup'

    """

    form_class = None
    url_name = None

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update({
            'form': self.form_class(),
            'action': self.get_form_action(instance),
        })
        return context

    @property
    def view_name(self):
        """
        a string with the default application namespace (defined in cms_apps.py) and the url_name
        e.g 'living:signup'
        """
        return '{}:{}'.format(self.model._meta.app_label, self.url_name)

    def get_form_action(self, instance):
        """ reversed url. For the view, to send the form data to. """
        return reverse(self.view_name, kwargs={'plugin_id': instance.id})


class AllinkBaseSectionPluginForm(AllinkMediaAdminMixin, forms.ModelForm):
    class Meta:
        model = AllinkBaseSectionPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkBaseSectionPluginForm, self).__init__(*args, **kwargs)

        self.fields['columns'] = forms.ChoiceField(
            label='Columns',
            choices=self._meta.model.COLUMNS,
            initial=self._meta.model.COLUMNS[0][0],
            required=True)
        if len(self._meta.model.COLUMNS) <= 1:
            self.fields['columns'].widget = forms.HiddenInput()

        self.fields['column_order'] = forms.ChoiceField(
            label='Column Order',
            choices=self._meta.model.COLUMN_ORDERS,
            initial=self._meta.model.COLUMN_ORDERS[0][0],
            required=True)
        if len(self._meta.model.COLUMN_ORDERS) <= 1:
            self.fields['column_order'].widget = forms.HiddenInput()

        if get_additional_choices('SECTION_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predefined variations',
                choices=get_additional_choices('SECTION_CSS_CLASSES'),
                initial=get_additional_choices('SECTION_CSS_CLASSES_INITIAL'),
                required=False)

        self.fields['project_css_spacings_top_bottom'] = forms.ChoiceField(
            label='Spacings top & bottom',
            choices=get_additional_choices('SECTION_SPACINGS', blank=True),
            required=False)

        self.fields['project_css_spacings_top'] = forms.ChoiceField(
            label='Spacings top',
            choices=get_additional_choices('SECTION_SPACINGS', blank=True),
            required=False)

        self.fields['project_css_spacings_bottom'] = forms.ChoiceField(
            label='Spacings bottom',
            choices=get_additional_choices('SECTION_SPACINGS', blank=True),
            required=False)


class CMSAllinkBaseSectionPlugin(CMSPluginBase):
    model = AllinkBaseSectionPlugin
    module = 'allink modules'
    allow_children = True
    child_classes = []  # define this on a per plugin level
    form = AllinkBaseSectionPluginForm
    render_template = None  # define this on a per plugin level

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'columns',
                    'column_order',
                ),
            }),
            ('Spacings', {
                'fields': [
                    'project_css_spacings_top_bottom',
                    'project_css_spacings_top',
                    'project_css_spacings_bottom',
                ]
            }),
            ('Section Options', {
                'classes': ('collapse',),
                'fields': [
                    'project_css_classes',
                    'anchor',
                ]
            }),
        )
        return fieldsets
