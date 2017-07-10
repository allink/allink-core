from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='allink_styleguide/styleguide.html'), name='core'),
]
