# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView


app_name = 'allink_styleguide'

urlpatterns = [
    path('', TemplateView.as_view(template_name='allink_styleguide/styleguide.html'), name='core'),
]
