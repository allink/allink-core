# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from cms.plugin_base import CMSPluginBase

from ..models import AllinkBaseAppContentPlugin

from .forms import AllinkBaseAppContentPluginForm


class CMSAllinkBaseAppContentPlugin(CMSPluginBase):
    """
    is not registered itself
    only used to inherit from (for specific App Content Plugins)
    """
    model = AllinkBaseAppContentPlugin

    name = _('App Content')
    module = _("allink")
    cache = False
    allow_children = True
    child_classes = ['LinkPlugin', 'Bootstrap3ButtonCMSPlugin']
    form = AllinkBaseAppContentPluginForm
    data_model = model.data_model

    class Media:
        js = ('build/djangocms_custom_admin_style.js', )
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
                    'title',
                    'title_size',
                ),
            }),
        )



        fieldsets += (_('Display Options'), {
            'classes': ('collapse',),
            'fields': (
                'template',
                'container_enabled',
                'softpage_enabled',
                'bg_color',
            )
        }),

        if self.data_model.get_can_have_categories():
            fieldsets += (_('Filter & Ordering'), {
                'classes': ('collapse',),
                'fields': (
                    'categories',
                    'manual_ordering',
                )
            }),

        fieldsets += (_('Select entries manually'), {
            'classes': ('collapse',),
            'fields': (
                'manual_entries',
            )
        }),

        fieldsets += (_('Category Navigation Options'), {
            'classes': ('collapse',),
            'fields': (
                'category_navigation_enabled',
                'category_navigation_all',
            )
        }),

        fieldsets += (_('Grid Options'), {
            'classes': ('collapse',),
            'fields': (
                'items_per_row',
            )
        }),

        fieldsets += (_('Pagination Options'), {
            'classes': ('collapse',),
            'fields': (
                ('paginated_by', 'pagination_type', ),
                'load_more_button_text'
            )
        }),

        fieldsets += (_('Additional Options'), {
            'classes': ('collapse',),
            'fields': (
                'detail_link_text',
            )
        }),

        return fieldsets

    def get_render_template(self, context, instance, placeholder, file='content'):
        template = '{}/plugins/{}/{}.html'.format(self.data_model._meta.app_label, instance.template, file)
        try:
            get_template(template)
        except:
            template = 'app_content/plugins/{}/{}.html'.format(instance.template, file)
        return template


    def render(self, context, instance, placeholder):

        # manual entries
        if instance.manual_entries.exists():
            objects_list = instance.get_selected_entries()
        # category navigation and no category "all" (only first category is relevant)
        elif instance.category_navigation_enabled and not instance.category_navigation_all:
            objects_list = instance.get_render_queryset_for_display(category=instance.get_first_category())
        else:
            objects_list = instance.get_render_queryset_for_display()


        # Paginate Objects
        if instance.paginated_by > 0:
            paginator = Paginator(objects_list, instance.paginated_by)
            firstpage = paginator.page(1)
            objects_list = firstpage

            # Pagination Type
            if instance.pagination_type == AllinkBaseAppContentPlugin.LOAD and firstpage.has_next():
                context['page_obj'] = firstpage
                context.update({'next_page_url': reverse('{}:more'.format(self.data_model._meta.model_name), kwargs={'page': context['page_obj'].next_page_number()}) + '?api_request=1' + '&plugin_id={}'.format(instance.id)})
                if instance.category_navigation_enabled and not instance.category_navigation_all:
                    context['next_page_url'] = context['next_page_url'] + '&category={}'.format(instance.get_first_category().id)

        # category navigation
        if instance.category_navigation_enabled:
            context.update({'by_category': reverse('{}:more'.format(self.data_model._meta.model_name), kwargs={'page': 1}) + '?api_request=1' + '&plugin_id={}'.format(instance.id)})


        context['instance'] = instance
        context['placeholder'] = placeholder
        context['object_list'] = objects_list

        context['content_template'] = self.get_render_template(context, instance, placeholder, file='_content')
        context['item_template'] = self.get_render_template(context, instance, placeholder, file='item')
        context['category_navigation'] = instance.get_category_navigation()

        return context
