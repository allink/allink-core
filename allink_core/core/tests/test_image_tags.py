from unittest import mock
from django.test.testcases import TestCase, override_settings
from django.template import Context, Template

from easy_thumbnails.exceptions import InvalidImageFormatError
from allink_core.core.test.base import GenericPluginMixin
from allink_core.core.utils import get_ratio_w_h, get_height_from_ratio
from allink_core.core.test.factories import FilerImageFactory
from allink_core.core.templatetags.allink_image_tags import (
    get_sizes_from_width_alias, get_width_alias_from_column_plugin, render_image,
)
from allink_core.core_apps.allink_image.cms_plugins import CMSAllinkImagePlugin


class MockThumbnailer(mock.Mock):
    def get_thumbnail(*args, **kwargs):
        return None


""" as reference
THUMBNAIL_WIDTH_ALIASES = {
    '1-of-1': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 1200, 'ratio': '3-2'},
        'xl': {'width': 1500, 'ratio': '3-2'}
    },
    '1-of-2': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 650, 'ratio': '3-2'},
        'xl': {'width': 900, 'ratio': '3-2'}
    },
    '2-of-3': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 600, 'ratio': '3-2'},
        'xl': {'width': 800, 'ratio': '3-2'}
    },
    '1-of-3': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 400, 'ratio': '3-2'},
        'xl': {'width': 400, 'ratio': '3-2'}
    },
    '1-of-4': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 500, 'ratio': '3-2'},
        'xl': {'width': 500, 'ratio': '3-2'}
    },
    'test-original': {
        'xs': {'width': 450, 'ratio': 'x-y'},
        'sm': {'width': 500, 'ratio': 'x-y'},
        'xl': {'width': 500, 'ratio': 'x-y'}
    },
}
"""

THUMBNAIL_WIDTH_ALIASES_MISSING = {
    '1-of-1': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 1200, 'ratio': '3-2'},
        'xl': {'width': 1500, 'ratio': '3-2'}
    },
    '1-of-2': {
        'xs': {'width': 450, 'ratio': '3-2'},
        # 'sm': {'width': 650, 'ratio': '3-2'},  missing
        'xl': {'width': 900, 'ratio': '3-2'}
    },
}


class ImageTagsUtilsTestCase(TestCase):

    def test_get_ratio_w_h(self):
        ratio = '3-2'
        expected_w_h = (3, 2)
        result = get_ratio_w_h(ratio)
        self.assertEqual(expected_w_h, result)

    def test_get_height_from_ratio(self):
        width = 450
        ratio_w = 3
        ratio_h = 2

        expected_h = width * ratio_h / ratio_w  # 300

        result = get_height_from_ratio(width, ratio_w, ratio_h)
        self.assertEqual(expected_h, result)

    def test_get_sizes_from_width_alias(self):
        alias = '1-of-1'
        expected_sizes = [
            ('xs', (450, 300)),
            ('sm', (1200, 800)),
            ('xl', (1500, 1000)),
        ]
        result = get_sizes_from_width_alias(alias, image=None)
        self.assertListEqual(expected_sizes, result)

    def test_get_sizes_from_width_alias_original(self):
        alias = 'test-original'
        expected_sizes = [
            ('xs', (450, 225)),
            ('sm', (500, 250)),
            ('xl', (500, 250)),
        ]

        image = mock.MagicMock()
        image.width = 1000
        image.height = 500

        result = get_sizes_from_width_alias(alias, image=image)
        self.assertListEqual(expected_sizes, result)


class ImageTagsImagePluginUtilsTestCase(GenericPluginMixin, TestCase):
    plugin_class = CMSAllinkImagePlugin

    def test_get_width_alias_from_column_plugin_no_context_3(self):
        result = get_width_alias_from_column_plugin(self.plugin_model_instance)
        self.assertEqual('2-of-3', result)


class ImageTagsImagePluginContextTestCase(TestCase):
    """
    used width_alias:

    '1-of-4': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 500, 'ratio': '3-2'},
        'xl': {'width': 500, 'ratio': '3-2'}
    },

    expected context:
    {
        'instance': {'id': 1},

        'image', Image:

        'icon_enabled': True,
        'bg_enabled': True,
        'bg_color': None,
        'lazyload_enabled': True,
        'alt_text': '',
        'vh_enabled': False,

        'ratio_percent_xs': '66.66666666666666%',
        'ratio_vh_xs': '66.66666666666666vh',
        'thumbnail_xs', ThumbnailFile: filer_public_thumbnails/filer_public/a6/34/a634ad24-214f-400c-8957-90c3a23d3da0/so.png__450x300.0_q60_HIGH_RESOLUTION_crop-smart_subsampling-2_upscale.jpg>,

        'ratio_percent_sm': '66.66666666666666%',
        'ratio_vh_sm': '66.66666666666666vh',
        'thumbnail_sm', ThumbnailFile: filer_public_thumbnails/filer_public/a6/34/a634ad24-214f-400c-8957-90c3a23d3da0/so.png__600x400.0_q60_HIGH_RESOLUTION_crop-smart_subsampling-2_upscale.jpg>,

        'ratio_percent_xl': '66.66666666666667%',
        'ratio_vh_xl': '66.66666666666667vh',
        'thumbnail_xl', ThumbnailFile: filer_public_thumbnails/filer_public/a6/34/a634ad24-214f-400c-8957-90c3a23d3da0/so.png__800x533.3333333333334_q60_HIGH_RESOLUTION_crop-smart_subsampling-2_upscale.jpg>
    }
    """

    width_alias = '1-of-4'

    def setUp(self):
        super().setUp()
        self.dummy_plugin = mock.Mock(id=1)

        self.context = {
            'instance': self.dummy_plugin
        }
        self.image = FilerImageFactory()

    def test_context_default_values(self):
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('instance'), self.dummy_plugin)
        self.assertEqual(context.get('icon_enabled'), False)
        self.assertEqual(context.get('bg_enabled'), True)
        self.assertEqual(context.get('bg_color'), None)
        self.assertEqual(context.get('lazyload_enabled'), True)
        self.assertEqual(context.get('vh_enabled'), False)

    def test_context_ratio_values_xs(self):
        # 'xs': {'width': 450, 'ratio': '3-2'},
        w = 450
        h = w / 3 * 2

        expected_ration = '{}'.format(h / w * 100)  # 66.66666666666666
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('ratio_percent_sm'), '{}%'.format(expected_ration))
        self.assertEqual(context.get('ratio_vh_sm'), '{}vh'.format(expected_ration))

    def test_context_ratio_values_sm(self):
        # 'sm': {'width': 500, 'ratio': '3-2'},
        w = 500
        h = w / 3 * 2

        expected_ration = '{}'.format(h / w * 100)  # 66.66666666666666
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('ratio_percent_xs'), '{}%'.format(expected_ration))
        self.assertEqual(context.get('ratio_vh_xs'), '{}vh'.format(expected_ration))

    def test_context_ratio_values_xl(self):
        # 'xl': {'width': 500, 'ratio': '3-2'}
        w = 500
        h = w / 3 * 2

        expected_ration = '{}'.format(h / w * 100)  # 66.66666666666667
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('ratio_percent_xl'), '{}%'.format(expected_ration))
        self.assertEqual(context.get('ratio_vh_xl'), '{}vh'.format(expected_ration))

    @override_settings(THUMBNAIL_WIDTH_ALIASES=THUMBNAIL_WIDTH_ALIASES_MISSING)
    def test_missing_width_alias_in_second_render(self):
        """
        if two images are rendered on the same page with different width aliases
        and the second one is missing one size, the context of the first one is used. Which should not be used.
        """
        # first render
        context = render_image(self.context, self.image, width_alias='1-of-1')
        # use context from first render (ike this is what is the case when calling render_image in a template twice)
        context = render_image(context, self.image, width_alias='1-of-2')
        self.assertIsNone(context.get('thumbnail_sm'))

    @mock.patch('allink_core.core.templatetags.allink_image_tags.get_unique_key')
    def test_picture_id_instance(self, mock_get_unique_key):
        mock_get_unique_key.return_value = 1
        context = render_image(self.context, self.image, width_alias='1-of-1')
        self.assertEqual(context.get('picture_id'), f'picture-{self.image.id}-1-1500-1000')

    @mock.patch('allink_core.core.templatetags.allink_image_tags.get_unique_key')
    def test_picture_id_instance_none(self, mock_get_unique_key):
        mock_get_unique_key.return_value = 1
        ctx_no_instance = {}
        context = render_image(ctx_no_instance, self.image, width_alias='1-of-1')

        self.assertEqual(context.get('picture_id'), f'picture-{self.image.id}-1-1500-1000')

    @mock.patch('allink_core.core.templatetags.allink_image_tags.get_thumbnailer', MockThumbnailer)
    def test_image_does_not_exist(self):
        """ if the image does not exist, no exception should not thrown """
        with mock.patch.object(MockThumbnailer, 'get_thumbnail') as mock_method:
            mock_method.side_effect = InvalidImageFormatError
            context = render_image(self.context, self.image, width_alias=self.width_alias)
            self.assertIsNone(context.get('thumbnail_xl'))

    @mock.patch('allink_core.core.templatetags.allink_image_tags.get_thumbnailer', MockThumbnailer)
    def test_thumbnail_options_default_values(self):
        # 'xl': {'width': 500, 'ratio': '3-2'}
        w = 500
        h = w / 3 * 2

        expected_thumbnail_options = {
            'crop': 'smart', 'bw': False, 'upscale': True, 'HIGH_RESOLUTION': True, 'zoom': None,
            'subject_location': self.image.subject_location, 'size': (w, h),
        }
        with mock.patch.object(MockThumbnailer, 'get_thumbnail') as mock_method:
            render_image(self.context, self.image, width_alias=self.width_alias)

            mock_method.assert_called_with(expected_thumbnail_options)
            self.assertEqual(mock_method.call_count, 3)


class ImageTagsImagePluginRenderTestCase(TestCase):
    """
    used width_alias:

    '1-of-4': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 500, 'ratio': '3-2'},
        'xl': {'width': 500, 'ratio': '3-2'}
    },
    """

    def setUp(self):
        super().setUp()
        self.dummy_plugin = mock.Mock(id=1)
        self.context = {
            'instance': self.dummy_plugin
        }
        self.image = FilerImageFactory()
        self.sizes = {
            'xs': "450x{}".format(450 / 3 * 2),
            'sm': "500x{}".format(500 / 3 * 2),
            'xl': "500x{}".format(500 / 3 * 2),
        }

    def test_context_render_all_image_urls(self):
        context = Context({
            'instance': self.dummy_plugin,
            'image': self.image,

        })
        template_to_render = Template(
            '{% load allink_image_tags %}'
            '{% render_image image width_alias="1-of-4" %}'
        )
        rendered_template = template_to_render.render(context)

        for size in self.sizes.items():
            self.assertIn('{}__{}'.format(self.image.original_filename, size[1]), rendered_template)
