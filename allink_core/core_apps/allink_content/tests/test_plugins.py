# # -*- coding: utf-8 -*-
# import os
# from django.test import TestCase
# from django.test.client import RequestFactory
# from django.template.loader import render
#
# from cms.api import add_plugin
# from cms.models import Placeholder
# from cms.plugin_rendering import ContentRenderer
#
# import allink_core.djangocms_content as app
# from ..cms_plugins import CMSAllinkContentPlugin, CMSAllinkContentColumnPlugin
#
#
# APP_NAME = app.__name__.split('.')[-1]
# TEMPLATE_DIR = os.path.join(os.path.dirname(app.__file__), 'templates', APP_NAME)
#
# class CMSAllinkContentPluginTest(TestCase):
#
#     def test_plugin_html(self):
#         placeholder = Placeholder.objects.create(slot='test')
#         model_instance = add_plugin(
#             placeholder,
#             CMSAllinkContentPlugin,
#             'en',
#         )
#         renderer = ContentRenderer(request=RequestFactory())
#         html = renderer.render_plugin(model_instance, {})
#         self.assertEqual(html, render_to_string(os.path.join(TEMPLATE_DIR, 'default/content.html')))
#
#
# class CMSAllinkContentColumnPluginTest(TestCase):
#
#     def test_plugin_html(self):
#         placeholder = Placeholder.objects.create(slot='test')
#         model_instance = add_plugin(
#             placeholder,
#             CMSAllinkContentColumnPlugin,
#             'en',
#         )
#         renderer = ContentRenderer(request=RequestFactory())
#         html = renderer.render_plugin(model_instance, {})
#         self.assertEqual(html, render_to_string(os.path.join(TEMPLATE_DIR, 'default/column.html')))
#
