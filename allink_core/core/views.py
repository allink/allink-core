# -*- coding: utf-8 -*-

import json
import urllib.parse
import re

from django.views.generic import ListView, DetailView, CreateView, FormView
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist

from parler.views import TranslatableSlugMixin

from allink_core.core.models.models import AllinkBaseAppContentPlugin
from allink_core.core_apps.allink_categories.models import AllinkCategory
from allink_core.core.utils import get_query


class AllinkBasePluginLoadMoreView(ListView):
    """
    model =
    plugin_model =
    """

    def get_queryset(self):
        if self.plugin.manual_ordering == AllinkBaseAppContentPlugin.RANDOM:
            queryset, path = self.request.session.get("random_plugin_queryset_%s" % self.plugin.id, ([], None))
            if (queryset and path == self.request.path) or not queryset:
                queryset = list(self.get_queryset_by_category())
                self.request.session["random_plugin_queryset_%s" % self.plugin.id] = (queryset, self.request.path)
        else:
            queryset = self.get_queryset_by_category()
        return queryset

    def get_queryset_by_category(self):
        filters = {re.sub('filter-%s-' % self.plugin.data_model._meta.model_name, '', k): urllib.parse.unquote_plus(v) for k, v in self.request.GET.items() if (k.startswith('filter-%s-' % self.plugin.data_model._meta.model_name) and v != 'None')}
        if self.plugin.manual_entries.exists():
            if hasattr(self, 'category'):
                return self.plugin.get_selected_entries(filters=filters).filter_by_category(self.category)
            else:
                return self.plugin.get_selected_entries(filters=filters)
        if hasattr(self, 'category'):
            return self.plugin.get_render_queryset_for_display(category=self.category, filters=filters)
        else:
            return self.plugin.get_render_queryset_for_display(filters=filters)

    def get_paginate_by(self, queryset):
        if self.plugin.paginated_by != 0:
            return self.plugin.paginated_by
        else:
            return None

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            if self.plugin.pagination_type == AllinkBaseAppContentPlugin.LOAD_REST:
                # TODO is there a better query?
                queryset = self.get_queryset().filter(~Q(id__in=[o.id for o in paginator.page(1).object_list]))
                page = paginator.page(paginator.num_pages)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return context

    def get_template_names(self, context):
        file = 'no_results' if not context['object_list'] else '_items'
        return [self.plugin.get_correct_template(file)]

    def get(self, request, *args, **kwargs):
        if 'plugin_id' in request.GET.keys():
            self.plugin = self.plugin_model.objects.get(cmsplugin_ptr_id=request.GET.get('plugin_id'))
            if 'category' in request.GET.keys():
                self.category_id = request.GET.get('category', None)
                self.category = AllinkCategory.objects.get(id=self.category_id)
                self.object_list = self.get_queryset()
            else:
                self.object_list = self.get_queryset()
        else:
            self.object_list = self.model.objects.all()

        context = self.get_context_data()
        context.update({'request': request})

        if 'api_request' in request.GET.keys():
            return self.json_response(context)
        return self.render_to_response(context)

    def json_response(self, context):
        context.update({'request': self.request})
        context.update({'instance': self.plugin})
        context.update({'is_ajax': True})
        if self.plugin.paginated_by > 0:
            if context['page_obj'].number > 1:
                context.update({'appended': True})
        json_context = {}
        json_context['rendered_content'] = render_to_string(self.get_template_names(context)[0], context=context, request=self.request)
        if self.plugin.paginated_by > 0 and context['page_obj'].has_next():  # no need to create next_page_url when no pagination should be displayed
            get_params = '&'.join(['%s=%s' % (k, v) for k, v in self.request.GET.items()])
            json_context['next_page_url'] = reverse('{}:more'.format(self.model._meta.model_name), kwargs={'page': context['page_obj'].next_page_number()}) + '?api_request=1&plugin_id={}&{}'.format(self.plugin.id, get_params)
            json_context['next_page_url'] = json_context['next_page_url'] + '&category={}'.format(self.category_id) if hasattr(self, 'category_id') else json_context['next_page_url']
        else:
            json_context['next_page_url'] = None
        json_context['no_results'] = False if self.object_list else True
        return HttpResponse(content=json.dumps(json_context), content_type='application/json', status=200)


class AllinkBaseDetailView(TranslatableSlugMixin, DetailView):
    """
    model = Events
    """
    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            context.update({'base_template': 'app_content/ajax_base.html'})
        else:
            context.update({'base_template': 'base.html'})
        return render_to_response(self.get_template_names(), context, context_instance=RequestContext(self.request))


class AllinkBaseCreateView(CreateView):
    """
    form_class =
    template_name  =
    success_url =
    """
    plugin = None

    def form_invalid(self, form):
        """
         If the form is invalid, re-render the context data with the
         data-filled form and errors.
        """
        if self.request.is_ajax():
            return self.render_to_response(self.get_context_data(form=form), status=206)
        else:
            return super(AllinkBaseCreateView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            context = self.get_context_data()
            try:
                return self.json_response(context)
            except:
                # sentry is not configured on localhost
                if not settings.RAVEN_CONFIG.get('dsn'):
                    raise
                form.add_error(None, _(u'Something went wrong with your subscription. Please try again later.'))
                return self.render_to_response(self.get_context_data(form=form), status=206)
        else:
            return HttpResponseRedirect(self.get_success_url())

    def json_response(self, context):
        json_context = {}
        json_context['rendered_content'] = render_to_string(self.get_confirmation_template(), context=context, request=self.request)
        return HttpResponse(content=json.dumps(json_context), content_type='application/json', status=200)

    def get_context_data(self, *args, **kwargs):
        context = super(AllinkBaseCreateView, self).get_context_data(*args, **kwargs)
        # EventsRegister view doesn't have a plugin instance
        if self.plugin:
            context.update({'instance': self.plugin})
            context.update({'inline': True if self.plugin._meta.model_name != 'allinkbuttonlinkplugin' else False})
        return context

    def get_confirmation_template(self):
        template = '{}/forms/confirmation.html'.format(self.model._meta.app_label)
        try:
            get_template(template)
        except TemplateDoesNotExist:
            template = 'partials/forms/confirmation.html'
        return template


class AllinkBaseAjaxFormView(FormView):
    """
    form_class =
    plugin_class =
    template_name = '.../plugins/search/_items.html'
    """

    def dispatch(self, *args, **kwargs):
        plugin_id = self.kwargs.pop('plugin_id', None)
        self.plugin = self.plugin_class.objects.get(id=plugin_id)
        return super(AllinkBaseAjaxFormView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AllinkBaseAjaxFormView, self).get_context_data(*args, **kwargs)
        context.update({'instance': self.plugin})
        return context

    def get_object_list(self, query_string):
        if query_string:
            entry_query = get_query(query_string, ['translations__title', 'translations__lead'])
            object_list = self.plugin.data_model.objects.active().filter(entry_query).distinct()
        else:
            object_list = self.plugin.data_model.objects.active().all().distinct()
        return object_list

    def form_valid(self, form):
        context = self.get_context_data()

        context.update({'object_list': self.get_object_list(form.cleaned_data.get('q'))})
        context.update({'csrf_token_value': self.request.COOKIES['csrftoken']})

        return self.json_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=206)

    def json_response(self, context):
        context.update({'request': self.request})
        context.update({'instance': self.plugin})

        json_context = {}
        json_context['rendered_content'] = render_to_string(self.template_name, context=context, request=self.request)
        json_context['no_results'] = False if context['object_list'] else True
        return HttpResponse(content=json.dumps(json_context), content_type='application/json', status=200)


# used to redirect page to external url
def external_view(request, target):
    return HttpResponsePermanentRedirect('http://' + target)