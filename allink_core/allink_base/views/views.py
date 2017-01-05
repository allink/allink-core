# -*- coding: utf-8 -*-
import json

from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

from parler.views import TranslatableSlugMixin

class AllinkBasePluginLoadMoreView(ListView):

    def get_queryset(self):
        queryset = self.plugin.get_render_queryset_for_display()
        return queryset

    def get_paginate_by(self, queryset):
        if self.plugin.paginated_by != 0:
            return self.plugin.paginated_by
        else:
            return None

    def get_template_names(self, file='_content'):
        opts = self.plugin_model._meta
        template = '{}/plugins/{}/{}.html'.format(opts.app_label, self.plugin.template, file)
        try:
            get_template(template)
        except:
            template = 'app_content/plugins/{}/{}.html'.format(self.plugin.template, file)
        return [template]

    def get(self, request, *args, **kwargs):
        if 'plugin_id' in request.GET.keys():
            self.plugin = self.plugin_model.objects.get(cmsplugin_ptr_id=request.GET.get('plugin_id'))
            if 'category' in request.GET.keys():
                self.category_id = request.GET.get('category', None)
                self.object_list = self.get_queryset().filter(categories=request.GET.get('category'))
            else:
                self.object_list = self.get_queryset()
        else:
            self.object_list = self.model.objects.all()

        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                              % {'class_name': self.__class__.__name__})

        context = self.get_context_data()
        context.update({'request': request})

        context.update({'content_template': self.get_template_names(file='_content')[0]})
        context.update({'item_template': self.get_template_names(file='item')[0]})

        if 'api_request' in request.GET.keys():
            return self.json_response(context)
        return self.render_to_response(context)

    def json_response(self, context):
        context.update({'request': self.request})
        context.update({'instance': self.plugin})
        if self.plugin.paginated_by > 0:
            if context['page_obj'].number > 1:
                context.update({'appended': True})
        json_context = {}
        json_context['rendered_content'] = render_to_string(self.get_template_names()[0], context=context, request=context['request'])
        if self.plugin.paginated_by > 0 and context['page_obj'].has_next():  # no need to create next_page_url when no pagination should be displayed
            json_context['next_page_url'] = reverse('{}:more'.format(self.model._meta.model_name), kwargs={'page': context['page_obj'].next_page_number()}) + '?api_request=1&plugin_id={}'.format(self.plugin.id)
            json_context['next_page_url'] = json_context['next_page_url'] + '&category={}'.format(self.category_id) if hasattr(self, 'category_id') else json_context['next_page_url']
        else:
            json_context['next_page_url'] = None
        return HttpResponse(content=json.dumps(json_context), content_type='application/json')


class AllinkBaseDetailView(TranslatableSlugMixin, DetailView):
    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            context.update({'base_template': 'app_content/ajax_base.html'})
        return render_to_response(self.get_template_names(), context, context_instance=RequestContext(self.request))
