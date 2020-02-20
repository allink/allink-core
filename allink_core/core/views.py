# -*- coding: utf-8 -*-
import json
from django.views.generic import ListView, DetailView, FormView
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404, JsonResponse
from django.template.loader import render_to_string
from parler.views import TranslatableSlugMixin

from allink_core.core.models import AllinkBaseAppContentPlugin
from allink_core.core_apps.allink_categories.models import AllinkCategory
from allink_core.core.utils import update_context_google_tag_manager


class AllinkBasePluginLoadMoreView(ListView):

    plugin_model = None

    def get_queryset(self):
        if hasattr(self, 'category'):
            return self.plugin.get_render_queryset_for_display(category=self.category)
        else:
            return self.plugin.get_render_queryset_for_display()

    def get_paginate_by(self, queryset):
        if self.plugin.paginated_by != 0:
            return self.plugin.paginated_by
        else:
            return None

    def get_context_data(self, **kwargs):
        context = {
            'request': self.request,
            'instance': self.plugin,
            'appended': True
        }
        queryset = kwargs.pop('object_list', self.object_list)
        page_size = self.get_paginate_by(queryset)

        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            if self.plugin.pagination_type == AllinkBaseAppContentPlugin.LOAD_REST:
                # !! WARNING: the paginator and page_obj are not set correctly. Only the queryset is correct.
                # Yeah, not so pretty. But we couldn't find a way to alternate page_size with the django paginator.
                # this would probably be better moved to a separate view. (e.g AllinkBasePluginLoadRestView, which
                # takes the plugin id, a list of ids to be excluded from the queryset.)

                # exclude the first page from the full queryset
                queryset = self.get_queryset().filter(~Q(id__in=[o.id for o in paginator.page(1).object_list]))
                page = paginator.page(paginator.num_pages)  # fake the page to be the last page
            context.update({
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            })
        else:
            context.update({
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            })
        context.update(kwargs)
        return context

    def get_template_names(self, context):
        file = 'no_results' if not context['object_list'] else '_items'
        return [self.plugin.get_correct_template(file)]

    def get(self, request, *args, **kwargs):
        try:
            self.plugin = self.plugin_model.objects.get(cmsplugin_ptr_id=request.GET.get('plugin_id'))
            if 'category' in request.GET.keys():
                self.category_id = request.GET.get('category', None)
                self.category = AllinkCategory.objects.get(id=self.category_id)

        except (KeyError, self.plugin_model.DoesNotExist) as e:
            # this view is useless when we do not ha a plugin_id
            # or a plugin instance where we can get our information from
            raise Http404(e)

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.json_response(context)

    def json_response(self, context):
        json_context = {}

        json_context['rendered_content'] = render_to_string(
            self.get_template_names(context)[0], context=context,
            request=self.request
        )

        # no need to create next_page_url when no pagination should be displayed
        if self.plugin.paginated_by > 0:

            if context['page_obj'].has_next():
                get_params = '&'.join(['%s=%s' % (k, v) for k, v in self.request.GET.items()])

                json_context['next_page_url'] = reverse(
                    '{}:more'.format(self.plugin.data_model._meta.model_name),
                    kwargs={'page': context['page_obj'].next_page_number()}
                ) + '?{}'.format(get_params)

                json_context['next_page_url'] = json_context['next_page_url'] + '&category={}'.format(
                    self.category_id) if hasattr(self, 'category_id') else json_context['next_page_url']
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


class AllinkBasePluginAjaxFormView(FormView):
    """
    Use this class whenever you create a plugin which displays a form.

    example implementation:

    class ProductTrackingView(AllinkBasePluginAjaxFormView):
        form_class = ProductTrackingForm
        template_name = 'product/plugins/tracking/content.html'

        success_template_name = 'product/plugins/tracking/success.html'
        plugin_model = ProductTrackingPlugin

    example urls.py:
    path('tracking/(<int:plugin_id>/', ProductTrackingView.as_view(), name='tracking'),

    to ensure that search engines do not index the view when called with GET (unstyled),
    we only allow POST (the GET is with the cmsplugin render)
    http_method_names = ['post']

    therefore views inherit from this class are not suitable for direct links
    e.g all viewnames listed in BUTTON_LINK_SPECIAL_LINKS_CHOICES.
    these views will be called by a GET request and not with ajax
    """

    http_method_names = ['post']

    def post(self, request, plugin_id, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.

        adds the plugin instance from the plugin_id kwargs
        """
        self.plugin_instance = self.plugin_model.objects.get(id=plugin_id)
        _, self.plugin = self.plugin_instance.get_plugin_instance()

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
            'instance': self.plugin_instance,
            'action': self.plugin.get_form_action(self.plugin_instance),
        })
        # to be removed? because we could actually track the form with ""
        context = update_context_google_tag_manager(
            context=context,
            page_name=self.request.current_page.__str__(),
            page_id=self.request.current_page.id,
            plugin_id=self.plugin_instance,
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


class AllinkBasePluginAjaxCreateView(AllinkBasePluginAjaxFormView):
    """
    Use this class whenever you create a plugin which displays a form.

    example implementation:

    class ProductTrackingView(AllinkBasePluginAjaxCreateView):
        model = ProductTracking
        form_class = ProductTrackingForm
        template_name = 'product/plugins/tracking/content.html'

        success_template_name = 'product/plugins/tracking/success.html'
        plugin_model = ProductTrackingPlugin

    example urls.py:
    path('tracking/(<int:plugin_id>/', ProductTrackingView.as_view(), name='tracking'),

    to ensure that search engines do not index the view when called with GET (unstyled),
    we only allow POST (the GET is with the cmsplugin render)
    http_method_names = ['post']

    therefore views inherit from this class are not suitable for direct links
    e.g all viewnames listed in BUTTON_LINK_SPECIAL_LINKS_CHOICES.
    these views will be called by a GET request and not with ajax
    """

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


# used to redirect CMSPage to external url
def external_view(request, target):
    return HttpResponsePermanentRedirect('http://' + target)
