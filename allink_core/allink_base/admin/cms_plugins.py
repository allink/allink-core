# -*- coding: utf-8 -*-
import re

from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.template import TemplateDoesNotExist
from cms.plugin_base import CMSPluginBase

from allink_core.allink_base.models import AllinkBaseAppContentPlugin
from allink_core.allink_base.admin import AllinkBaseAppContentPluginForm


class CMSAllinkBaseAppContentPlugin(CMSPluginBase):
    """
    is not registered itself
    only used to inherit from (for specific App Content Plugins)
    """
    model = AllinkBaseAppContentPlugin

    name = _('App Content')
    module = _("allink Apps")
    allow_children = True
    child_classes = ['LinkPlugin', 'Bootstrap3ButtonCMSPlugin']
    form = AllinkBaseAppContentPluginForm
    data_model = model.data_model

    class Media:
        js = ('build/djangocms_custom_admin_scripts.js', )
        css = {
            'all': ('build/djangocms_custom_admin_style.css', )
        }

    @classmethod
    def get_render_queryset(cls):
        return cls.model._default_manager.all()

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    # 'title',
                    # 'title_size',
                    'template',
                ),
            }),
        )

        fieldsets += (_('Display Options'), {
            'classes': ('collapse',),
            'fields': (
                # 'container_enabled',
                'detail_link_enabled',
                'softpage_enabled',
                'bg_color',
                # 'bg_image_outer_container',
            )
        }),

        if self.data_model.get_can_have_categories():
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

        if self.data_model.get_can_have_categories():
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
                ('paginated_by', ),
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
                'detail_link_text',
                'project_css_classes',
                # 'extra_css_classes',
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

    def get_render_template(self, context, instance, placeholder, file='content'):
        if isinstance(context['object_list'], list):
            queryset_not_empty = True if len(context['object_list']) > 0 else False
        else:
            queryset_not_empty = context['object_list'].exists()

        if queryset_not_empty:
            template = '{}/plugins/{}/{}.html'.format(self.data_model._meta.app_label, instance.template, file)
        else:
            template = '{}/plugins/{}/{}.html'.format(self.data_model._meta.app_label, instance.template, 'no_results')
        try:
            get_template(template)
        except TemplateDoesNotExist:
            if queryset_not_empty:
                template = 'app_content/plugins/{}/{}.html'.format(instance.template, file)
            else:
                template = 'app_content/plugins/{}/{}.html'.format(instance.template, 'no_results')
        return template

    def get_queryset_by_category(self, instance, filters):
        # manual entries
        if instance.manual_entries.exists():
            objects_list = instance.get_selected_entries(filters=filters)
        # category navigation and no category "all" (only first category is relevant)
        elif instance.category_navigation_enabled and not instance.category_navigation_all:
            objects_list = instance.get_render_queryset_for_display(category=instance.get_first_category(), filters=filters)
        else:
            objects_list = instance.get_render_queryset_for_display(filters=filters)
        return objects_list

    def render(self, context, instance, placeholder):
        # getting filter parameters and attributes
        filters = {re.sub('filter-%s-' % instance.data_model._meta.model_name, '', k): v for k, v in context['request'].GET.items() if (k.startswith('filter-%s-' % instance.data_model._meta.model_name) and v != 'None')}
        # random ordering needs sessioncaching for objects_list
        if instance.manual_ordering == AllinkBaseAppContentPlugin.RANDOM:
            objects_list, path = context['request'].session.get("random_plugin_queryset_%s" % instance.id, ([], None))
            if (objects_list and path == context['request'].path) or not objects_list:
                objects_list = list(self.get_queryset_by_category(instance, filters))
                context['request'].session["random_plugin_queryset_%s" % instance.id] = (objects_list, context['request'].path)
        # not random ordering
        else:
            objects_list = self.get_queryset_by_category(instance, filters)

        # Paginate Objects
        if instance.paginated_by > 0:
            paginator = Paginator(objects_list, instance.paginated_by)
            firstpage = paginator.page(1)
            objects_list = firstpage.object_list

            # Pagination Type
            if instance.pagination_type == AllinkBaseAppContentPlugin.LOAD and firstpage.has_next():
                context['page_obj'] = firstpage
                context.update({'next_page_url': reverse('{}:more'.format(self.data_model._meta.model_name), kwargs={'page': context['page_obj'].next_page_number()}) + '?api_request=1' + '&plugin_id={}'.format(instance.id)})
                if instance.category_navigation_enabled and not instance.category_navigation_all:
                    context['next_page_url'] = context['next_page_url'] + '&category={}'.format(instance.get_first_category().id)

        # category navigation
        if instance.category_navigation_enabled or instance.filter_fields:
            context.update({'by_category': reverse('{}:more'.format(self.data_model._meta.model_name), kwargs={'page': 1}) + '?api_request=1' + '&plugin_id={}'.format(instance.id)})

        # if instance.filter_fields:
        #     context.update({'filter_fields': instance.get_filter_fields_with_options()})

        context['instance'] = instance
        context['placeholder'] = placeholder
        context['object_list'] = objects_list

        context['content_template'] = self.get_render_template(context, instance, placeholder, file='_content')
        context['no_results_template'] = self.get_render_template(context, instance, placeholder, file='_no_results')
        context['item_template'] = self.get_render_template(context, instance, placeholder, file='item')
        context['category_navigation'] = instance.get_category_navigation()

        return context
