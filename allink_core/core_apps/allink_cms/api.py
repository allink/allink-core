# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
from cms.models.pagemodel import Page


class CMSPluginAPIView(RetrieveAPIView):
    """
    - this will return the rendered html for a specific plugin
    - it will not render child plugins
    - some plugins need the current_page, so you can pass an id as a GET param
    """
    permission_classes = (AllowAny, )
    lookup_field = 'id'
    queryset = CMSPlugin.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        instance, plugin = self.object.get_plugin_instance()

        from django.template import RequestContext
        from cms.plugin_rendering import ContentRenderer

        renderer = ContentRenderer(request)
        context = RequestContext(request)

        try:
            # if current_page is supplied, we care about the original request
            request.current_page = Page.objects.get(id=request.GET.get('current_page'))
            request.path_info = request.current_page.get_absolute_url(language=request.LANGUAGE_CODE)
        except (KeyError, Page.DoesNotExist):
            pass

        # Avoid errors if plugin require a request object
        # when rendering.
        context['request'] = request
        content = renderer.render_plugin(instance, context)

        response = HttpResponse(content)
        response['X-Robots-Tag'] = 'noindex'
        return response
