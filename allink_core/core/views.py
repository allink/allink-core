# -*- coding: utf-8 -*-

import json
import urllib.parse
import re

from django.views.generic import ListView, DetailView, CreateView, FormView
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from parler.views import TranslatableSlugMixin

from allink_core.core.models import AllinkBaseAppContentPlugin
from allink_core.core_apps.allink_categories.models import AllinkCategory
from allink_core.core.utils import get_query, update_context_google_tag_manager


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
        filters = {re.sub('filter-%s-' % self.plugin.data_model._meta.model_name, '', k): urllib.parse.unquote_plus(v)
                   for k, v in self.request.GET.items() if
                   (k.startswith('filter-%s-' % self.plugin.data_model._meta.model_name) and v != 'None')}
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
        json_context['rendered_content'] = render_to_string(self.get_template_names(context)[0], context=context,
                                                            request=self.request)
        # no need to create next_page_url when no pagination should be displayed
        if self.plugin.paginated_by > 0 and context['page_obj'].has_next():
            get_params = '&'.join(['%s=%s' % (k, v) for k, v in self.request.GET.items()])
            json_context['next_page_url'] = reverse('{}:more'.format(self.model._meta.model_name), kwargs={
                'page': context['page_obj'].next_page_number()}) + '?api_request=1&plugin_id={}&{}'.format(
                self.plugin.id, get_params)
            json_context['next_page_url'] = json_context['next_page_url'] + '&category={}'.format(
                self.category_id) if hasattr(self, 'category_id') else json_context['next_page_url']
        else:
            json_context['next_page_url'] = None
        json_context['no_results'] = False if self.object_list else True
        return HttpResponse(content=json.dumps(json_context), content_type='application/json', status=200)


class AllinkBaseDetailView(TranslatableSlugMixin, DetailView):
    """
    model = Events
    """

    def get_template_names(self):
        obj = self.get_object()
        context = self.get_context_data(object=obj)
        categories = context['object'].categories.all()
        app_label = context['object']._meta.app_label
        templates = ['{}/{}_detail.html'.format(app_label, self.request.current_page.application_namespace)]
        templates += ['{}/{}_{}_detail.html'.format(app_label, app_label, category.slug) for category in categories]
        templates += super().get_template_names()
        return templates

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_staff and self.object.status == self.object.INACTIVE:
            raise Http404(_("The requested content is not published.") % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('softpage', None):
            context.update({'base_template': 'app_content/ajax_base.html'})
        return render(self.request, self.get_template_names(), context)


class AllinkBaseCreateView(CreateView):
    """
    form_class =
    template_name  =
    success_url =
    """
    plugin = None

    def get(self, request, *args, **kwargs):
        self.object = None
        response = super(AllinkBaseCreateView, self).get(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex'
        return response

    def form_invalid(self, form):
        """
         If the form is invalid, re-render the context data with the
         data-filled form and errors.
        """
        if self.request.is_ajax():
            return self.json_response(self.get_context_data(form=form), self.template_name, 206)
        else:
            return super(AllinkBaseCreateView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            context = self.get_context_data()
            try:
                return self.json_response(context, self.get_confirmation_template(), 200)
            except:
                # sentry is not configured on localhost
                if not settings.RAVEN_CONFIG.get('dsn'):
                    raise
                form.add_error(None, _('Something went wrong with your subscription. Please try again later.'))
                return self.render_to_response(self.get_context_data(form=form), status=206)
        else:
            return HttpResponseRedirect(self.get_success_url())

    def json_response(self, context, template, status):
        json_context = {}
        json_context['rendered_content'] = render_to_string(template, context=context, request=self.request)
        return HttpResponse(content=json.dumps(json_context), content_type='application/json', status=status)

    def get_context_data(self, *args, **kwargs):
        context = super(AllinkBaseCreateView, self).get_context_data(*args, **kwargs)
        plugin_id = getattr(self.plugin, 'id') if self.plugin else None
        context = update_context_google_tag_manager(context, self.request.current_page.__str__(),
                                                    self.request.current_page.id, plugin_id, self.__class__.__name__)
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


# deprecated (only really used by WorkSearchAjaxView) will be renamed in AllinkBaseAjaxSearchFormView
class AllinkBaseAjaxFormView(FormView):
    """
    form_class =
    plugin_class =
    """
    search_fields = ['translations__title', 'translations__lead']

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
            entry_query = get_query(query_string, self.search_fields)
            object_list = self.plugin.data_model.objects.active().filter(entry_query).distinct()
        else:
            object_list = self.plugin.data_model.objects.active()
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
        json_context['rendered_content'] = render_to_string(self.get_template_names()[0], context=context,
                                                            request=self.request)
        json_context['no_results'] = False if context['object_list'] else True
        return HttpResponse(content=json.dumps(json_context), content_type='application/json', status=200)


class AllinkBasePluginAjaxFormView(FormView):
    """
    Use this class whenever you create a plugin which displays a form.

    example implementation:

    class ProductTrackingView(AllinkBasePluginAjaxFormView):
        form_class = ProductTrackingForm
        template_name = 'product/plugins/tracking/content.html'

        success_template_name = 'product/plugins/tracking/success.html'
        plugin_class = ProductTrackingPlugin
        viewname = 'product:tracking'

    example urls.py:
    path('tracking/(<int:plugin_id>/', ProductTrackingView.as_view(), name='tracking'),

    to ensure that search engines do not index the view when called with GET (unstyled),
    we only allow POST (the GET is with the cmsplugin render)
    http_method_names = ['post']

    therefore views inherit from this clas are not suitable for direct links
    e.g all viewnames listed in BUTTON_LINK_SPECIAL_LINKS_CHOICES.
    these views will be called by a GET request and not with ajax
    """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.

        adds the plugin instance from the plugin_id kwargs
        """
        plugin_id = self.kwargs.pop('plugin_id', None)
        self.plugin = self.plugin_class.objects.get(id=plugin_id)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """
        Add the plugin instance context, so it ca be rendered with all necessary data
        and the same plugin template used by the cms
        """
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'csrf_token_value': self.request.COOKIES.get('csrftoken'),
            'request': self.request,
            'instance': self.plugin,
            'action': self.get_form_action(),
        })
        # to be removed? because we could actually track the form with ""
        context = update_context_google_tag_manager(
            context=context,
            page_name=self.request.current_page.__str__(),
            page_id=self.request.current_page.id,
            plugin_id=self.plugin,
            name=self.__class__.__name__
        )
        return context

    def form_valid(self, form):
        """
        We return the response as json, with status code 200
        """
        context = self.get_context_data(form=form)
        return self.get_json_response(
            context=context,
            status=200,
            template_name=self.get_success_template_names()[0]
        )

    def form_invalid(self, form):
        """
        We return the response as json, with status code 206
        """
        return self.get_json_response(
            context=self.get_context_data(form=form),
            status=206,
            template_name=self.get_template_names()[0]
        )

    def get_form_action(self):
        """
        Returns the reversed plugin url. which should points to this view.
        """
        return reverse(self.viewname, kwargs={'plugin_id': self.plugin.id})

    def get_success_template_names(self):
        """
        Returns a list of template names to be used for the successfull request. Must return
        a list. May not be called if form_valid is overridden.
        """
        if self.success_template_name is None:
            raise ImproperlyConfigured(
                "AllinkBasePluginAjaxFormView requires either a definition of "
                "'success_template_name' or an implementation of 'get_success_template_names()'")
        else:
            return [self.success_template_name]

    def get_json_response(self, context, status, template_name=None, data=None):
        """
        This response will most likely be handled by allink-core-static/js/modules/ajax-form.js

        context: the context which will we passed to template_name
        template_name: the template to render with
        status: 200 or 206, most likely
        data: additional response data (e.g 'success_url')

        * there is no template needed, when we redirect to a success_url
        """
        if not data:
            data = dict()

        if template_name:
            data.update({
                'rendered_content': render_to_string(template_name, context=context, request=self.request)
            })
        return JsonResponse(data, status=status)


# TODO
# class AllinkBaseAjaxPluginSearchFormView(AllinkBasePluginAjaxFormView):
#     """
#     example implementation:
#     class WorkSearchView
#     form_class = WorkSearchForm
#     template_name = 'work/plugins/search/content.html'
#
#     success_template_name = 'work/plugins/search/success.html' ?!
#     plugin_class = WorkSearchPlugin
#     viewname = 'work:search'
#
#     search_fields = ['translations__title', 'translations__lead']
#     """
#
#     search_fields = ['translations__title', 'translations__lead']
#
#     def get_object_list(self, query_string):
#         if query_string:
#             entry_query = get_query(query_string, self.search_fields)
#             object_list = self.plugin.data_model.objects.active().filter(entry_query).distinct()
#         else:
#             object_list = self.plugin.data_model.objects.active()
#         return object_list
#
#     def form_valid(self, form):
#         """
#         - adds the serach result queryset to the context
#         - adds no_results to json response, if empty queryset
#         """
#         context = self.get_context_data()
#         context.update({'object_list': self.get_object_list(form.cleaned_data.get('q'))})
#         data = {'no_results': False if context['object_list'] else True}
#
#         return self.get_json_response(
#             context=context,
#             status=200,
#             template_name=self.get_template_names()[0],
#             data=data
#         )

# TODO
# class AllinkBaseAjaxPluginCreateView(AllinkBasePluginAjaxFormView):
#     """
#     # example implementation:
#     # class OrderRequestView
#     #     model = OrderRequest
#     #     form_class = OrderRequestForm
#     #     template_name = 'order/plugins/request/content.html'
#     #
#     #     success_template_name = 'order/plugins/request/success.html'
#     #     plugin_class = OrderRequestPlugin
#     #     viewname = 'order:request'
#     """
#     plugin = None
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return super().form_valid(form)


# used to redirect CMSPage to external url
def external_view(request, target):
    return HttpResponsePermanentRedirect('http://' + target)
