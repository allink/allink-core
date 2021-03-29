from cms import api
from allink_core.core.test.base import PageApphookMixin
from django.test.testcases import TestCase
from allink_core.core_apps.allink_image.cms_plugins import CMSAllinkImagePlugin
from allink_core.core_apps.allink_content.cms_plugins import CMSAllinkContentPlugin, CMSAllinkContentColumnPlugin
from allink_core.core.templatetags.allink_image_tags import (
    get_width_alias_from_column_plugin,
)

class ImageTagsContentPluginUtilsTestCase(PageApphookMixin, TestCase):
    template = 'col-1'
    position = 1  #

    def setUp(self):
        super().setUp()
        # AllinkContentPlugin, template='col-1'
        self.content_plugin = api.add_plugin(
            self.placeholder,
            CMSAllinkContentPlugin,
            self.language,
            template=self.template
        )
        # AllinkContentColumnPlugin, template='col-1'
        column_amount = CMSAllinkContentPlugin.model.get_template_column_count(self.content_plugin.template)

        for x in range(int(column_amount)):
            api.add_plugin(
                self.placeholder,
                CMSAllinkContentColumnPlugin,
                self.language,
                target=self.content_plugin
            )

        self.column_plugin = self.content_plugin.get_children()[self.position - 1]

        # AllinkImagePlugin, inside column plugin
        self.image_plugin = api.add_plugin(
            self.placeholder,
            CMSAllinkImagePlugin,
            self.language,
            target=self.column_plugin
        )

    def test_get_width_alias_from_column_plugin_no_context_1(self):
        """ template col-1 """

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('1-of-1', result)

    def test_get_width_alias_from_column_plugin_no_context_1_1(self):
        self.content_plugin.template = 'col-1-1'
        self.content_plugin.save()

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('1-of-2', result)

    def test_get_width_alias_from_column_plugin_no_context_1_2_pos_0(self):
        self.content_plugin.template = 'col-1-2'
        self.content_plugin.save()

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('1-of-3', result)

    def test_get_width_alias_from_column_plugin_no_context_1_2_pos_1(self):
        self.content_plugin.template = 'col-1-2'
        self.content_plugin.save()
        self.column_plugin.position = 1
        self.column_plugin.save()

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('2-of-3', result)

    def test_get_width_alias_from_column_plugin_no_context_2_1_pos_0(self):
        self.content_plugin.template = 'col-2-1'
        self.content_plugin.save()

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('2-of-3', result)

    def test_get_width_alias_from_column_plugin_no_context_2_1_pos_1(self):
        self.content_plugin.template = 'col-2-1'
        self.content_plugin.save()
        self.column_plugin.position = 1
        self.column_plugin.save()

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('1-of-3', result)

    def test_get_width_alias_from_column_plugin_no_context_3(self):
        self.content_plugin.template = 'col-3'
        self.content_plugin.save()

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('1-of-3', result)

    def test_get_width_alias_from_column_plugin_no_context_4(self):
        self.content_plugin.template = 'col-4'
        self.content_plugin.save()

        result = get_width_alias_from_column_plugin(self.image_plugin)
        self.assertEqual('1-of-4', result)
