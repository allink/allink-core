from django.test.client import RequestFactory
from django.test.testcases import TestCase
from allink_core.core.test import GenericPluginMixin
from allink_core.core.customisation.dummy_new_app_form.cms_apps import DummyAppApphook
from allink_core.core.customisation.dummy_new_app_form.cms_plugins import CMSDummyAppSignupPlugin


class CMSDummyAppSignupPluginTestCaseApp(GenericPluginMixin, TestCase):
    apphook = DummyAppApphook.name
    namespace = DummyAppApphook.app_name
    page_template = 'default.html'
    apphook_object = DummyAppApphook

    plugin_class = CMSDummyAppSignupPlugin
    init_kwargs = {
        'from_email_address': 'test@allink.ch'
    }

    def test_context_object_list_all(self):
        plugin = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory()}
        context = plugin.render(context, self.plugin_model_instance, None)

        self.assertIsInstance(context['form'], self.plugin_class.form_class)
        self.assertEqual(context['action'], self.plugin_class.get_form_action(self.plugin_model_instance))
