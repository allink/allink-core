# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.generic import ListView, DetailView, CreateView

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist

from allink_core.allink_base.models import AllinkBaseAppContentPlugin

from parler.views import TranslatableSlugMixin

from allink_core.allink_categories.models import AllinkCategory


class AllinkBasePluginLoadMoreView(ListView):

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
        if hasattr(self, 'category'):
            return self.plugin.get_render_queryset_for_display(category=self.category)
        else:
            return self.plugin.get_render_queryset_for_display()

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
                self.category = AllinkCategory.objects.get(id=self.category_id)
                self.object_list = self.get_queryset()
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


class AllinkBaseCreateView(CreateView):
    """
        form_class =
        template_name  =
        success_url =
    """

    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            return JsonResponse({}, status=200)
        else:
            return HttpResponseRedirect(self.get_success_url())

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
            context = super(AllinkBaseCreateView, self).get_context_data()
            try:
                form.save()
                html = render_to_string(self.get_confirmation_template(), context)
                return HttpResponse(html)
            except:
                # sentry is not configured on localhost
                if not settings.RAVEN_CONFIG.get('dns'):
                    raise
                form.add_error(None, _(u'Something went wrong with your subscription. Please try again later.'))
                return self.render_to_response(self.get_context_data(form=form), status=206)
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_confirmation_template(self):
        template = '{}/forms/confirmation.html'.format(self.item._meta.model_name)
        try:
            get_template(template)
        except TemplateDoesNotExist:
            template = 'includes/forms/confirmation.html'
        return template

# class AllinkBaseRegistrationView(AllinkBaseCreateView):
#     """
#         model = CoursesRegistration
#         form_class = CoursesRegistrationForm
#         template_name = 'blog/events_register_detail.html'
#         item_model = Courses
#     """
#
#     def __init__(self):
#         super(AllinkBaseRegistrationView, self).__init__()
#         self.item = self.item_model.objects.get(translations__slug=self.kwargs.get('slug', None))
#
#     def get_context_data(self, **kwargs):
#         context = super(AllinkBaseCreateView, self).get_context_data(**kwargs)
#         context.update({
#             'slug': self.kwargs.get('slug', None)
#         })
#         return context
#
#     def get_initial(self):
#         initial = super(AllinkBaseRegistrationView, self).get_initial()
#         initial = initial.copy()
#         initial['item'] = self.item
#         initial['terms'] = AllinkTerms.objects.get_published()
#         return initial
#
#     def form_valid(self, form):
#         response = super(AllinkBaseRegistrationView, self).form_valid(form)
#         self.send_mail()
#         return response
#
#     def send_mail(self):
#         send_registration_email(self.get_form(), self.item)
#         send_registration_confirmation_email(self.get_form(), self.item)
