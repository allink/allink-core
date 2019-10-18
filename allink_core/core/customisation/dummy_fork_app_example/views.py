"""
use core:
no 'views.py' file needed
"""
from django.shortcuts import render
from allink_core.apps.dummy_app.views import DummyAppDetail as CoreDummyAppDetail


class DummyAppDetail(CoreDummyAppDetail):
    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('softpage', None):
            context.update({'base_template': 'app_content/ajax_base.html'})
        return render(self.request, self.get_template_names(), context)


# example for adding a new view.
from django.views.generic import TemplateView
from allink_core.core.loading import get_model

DummyApp = get_model('dummy_app', 'DummyApp')


class DummyAppSomeNewView(TemplateView):
    template_name = 'dummy_app/some_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        item = DummyApp.objects.new().first()
        context.update({'something_more_usefull': item.title})
        return context
