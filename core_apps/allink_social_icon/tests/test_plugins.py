# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from django.test.client import RequestFactory
from django.template.loader import render_to_string

from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer

import allink_core.core_apps.allink_social_icon as app
from allink_core.core_apps.allink_social_icon.cms_plugins import CMSAllinkSocialIconContainerPlugin, CMSAllinkSocialIconPlugin

APP_NAME = 'allink_social_icon'
TEMPLATE_DIR = os.path.join(os.path.dirname(app.__file__), 'templates', APP_NAME)


class CMSAllinkSocialIconContainerPluginTest(TestCase):

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            CMSAllinkSocialIconContainerPlugin,
            'en',
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        self.assertEqual(html, render_to_string(os.path.join(TEMPLATE_DIR, 'content.html')))


class CMSAllinkSocialIconPluginTest(TestCase):

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            CMSAllinkSocialIconPlugin,
            'en',
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        self.assertEqual(html, render_to_string(os.path.join(TEMPLATE_DIR, 'item.html')))
