# -*- coding: utf-8 -*-
from allink_core.allink_base.utils import get_height_from_ratio

####################################################################################

# =Thumbnail Sizes (Responsive and Retina ready)

# Docs: http://easy-thumbnails.readthedocs.io/en/2.1/usage/#thumbnail-aliases

THUMBNAIL_ALIASES = {
    '': {

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin > Video mobile image

        'video-mobile-image-xs': {'size': (320, get_height_from_ratio(450,4,3)), 'crop': 'scale', 'upscale': True},
        'video-mobile-image-xs-2x': {'size': (640, get_height_from_ratio(640,4,3)), 'crop': 'scale', 'upscale': True },
        'video-mobile-image-sm': {'size': (580, get_height_from_ratio(580,4,3)), 'crop': 'scale', 'upscale': True },
        'video-mobile-image-sm-2x': {'size': (1000, get_height_from_ratio(1000,4,3)), 'crop': 'scale', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # Content PLugin > Video Poster (while video is loading)

        'video-poster-image': {'size': (1400, get_height_from_ratio(1400,16,6)), 'crop': 'scale', 'upscale': True }, # ratio has to be the same as the video

        # # # # # # # # # # # # # # # # # # # # # #
        # Swiper (Slider): The slide's background image
        # Note: Make sure that the ratio passed to get_height_from_ratio() matched the ratio set in the CSS variables

        # > Displaying App Content as a Slider
        'slider-app-content-xs': {'size': (320, get_height_from_ratio(450,4,3)), 'crop': 'scale', 'upscale': True},
        'slider-app-content-xs-2x': {'size': (640, get_height_from_ratio(640,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-sm': {'size': (512, get_height_from_ratio(512,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-sm-2x': {'size': (1024, get_height_from_ratio(1024,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-md': {'size': (1030, get_height_from_ratio(1030,2,1)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-md-2x': {'size': (2060, get_height_from_ratio(2060,2,1)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-lg': {'size': (1200, get_height_from_ratio(1200,2,1)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-lg-2x': {'size': (2400, get_height_from_ratio(2400,2,1)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-xl': {'size': (1600, get_height_from_ratio(1600,2,1)), 'crop': 'scale', 'upscale': True },
        'slider-app-content-xl-2x': {'size': (2400, get_height_from_ratio(2400,2,1)), 'crop': 'scale', 'upscale': True },

        # > The header slider in an App Content's detail view
        'slider-detail-view-xs': {'size': (320, get_height_from_ratio(450,4,3)), 'crop': 'scale', 'upscale': True},
        'slider-detail-view-xs-2x': {'size': (640, get_height_from_ratio(640,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-sm': {'size': (512, get_height_from_ratio(512,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-sm-2x': {'size': (1024, get_height_from_ratio(1024,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-md': {'size': (1030, get_height_from_ratio(1030,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-md-2x': {'size': (2060, get_height_from_ratio(2060,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-lg': {'size': (1200, get_height_from_ratio(1200,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-lg-2x': {'size': (2400, get_height_from_ratio(2400,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-xl': {'size': (1600, get_height_from_ratio(1600,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-detail-view-xl-2x': {'size': (2400, get_height_from_ratio(2400,4,3)), 'crop': 'scale', 'upscale': True },

        # > Using the gallery plugin within a Content Plugin's Column
        'slider-gallery-plugin-xs': {'size': (320, get_height_from_ratio(450,4,3)), 'crop': 'scale', 'upscale': True},
        'slider-gallery-plugin-xs-2x': {'size': (640, get_height_from_ratio(640,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-sm': {'size': (512, get_height_from_ratio(512,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-sm-2x': {'size': (1024, get_height_from_ratio(1024,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-md': {'size': (1030, get_height_from_ratio(1030,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-md-2x': {'size': (2060, get_height_from_ratio(2060,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-lg': {'size': (1200, get_height_from_ratio(1200,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-lg-2x': {'size': (2400, get_height_from_ratio(2400,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-xl': {'size': (1600, get_height_from_ratio(1600,4,3)), 'crop': 'scale', 'upscale': True },
        'slider-gallery-plugin-xl-2x': {'size': (2400, get_height_from_ratio(2400,4,3)), 'crop': 'scale', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin: Parallax
        # The ratio for larger screen (from screen-md) is calculated as follows:
        # ($parallax-aspect-ratio-height-md) * ($parallax-bg-image-height) / 100
        'parallax-xs': {'size': (320, get_height_from_ratio(450,4,3)), 'crop': 'scale', 'upscale': True },
        'parallax-xs-2x': {'size': (640, get_height_from_ratio(640,4,3)), 'crop': 'scale', 'upscale': True },
        'parallax-sm': {'size': (512, get_height_from_ratio(512,4,3)), 'crop': 'scale', 'upscale': True },
        'parallax-sm-2x': {'size': (1024, get_height_from_ratio(1024,4,3)), 'crop': 'scale', 'upscale': True },
        'parallax-md': {'size': (1030, get_height_from_ratio(1030,3000,1690)), 'crop': 'scale', 'upscale': True },
        'parallax-md-2x': {'size': (2060, get_height_from_ratio(2060,3000,1690)), 'crop': 'scale', 'upscale': True },
        'parallax-lg': {'size': (1200, get_height_from_ratio(1200,3000,1690)), 'crop': 'scale', 'upscale': True },
        'parallax-lg-2x': {'size': (2400, get_height_from_ratio(2400,3000,1690)), 'crop': 'scale', 'upscale': True },
        'parallax-xl': {'size': (1600, get_height_from_ratio(1600,3000,1690)), 'crop': 'scale', 'upscale': True },
        'parallax-xl-2x': {'size': (2400, get_height_from_ratio(2400,3000,1690)), 'crop': 'scale', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin: Full-Height Mode

        'full-height-xs': {'size': (320, 420), 'crop': 'scale', 'upscale': True},
        'full-height-xs-2x': {'size': (640, 840), 'crop': 'scale', 'upscale': True },
        'full-height-sm': {'size': (512, 560), 'crop': 'scale', 'upscale': True },
        'full-height-sm-2x': {'size': (1024, 1120), 'crop': 'scale', 'upscale': True },
        'full-height-md': {'size': (1030, 840), 'crop': 'scale', 'upscale': True },
        'full-height-md-2x': {'size': (2060, 1280), 'crop': 'scale', 'upscale': True },
        'full-height-lg': {'size': (1200, 840), 'crop': 'scale', 'upscale': True },
        'full-height-lg-2x': {'size': (2400, 1280), 'crop': 'scale', 'upscale': True },
        'full-height-xl': {'size': (1600, 1000), 'crop': 'scale', 'upscale': True },
        'full-height-xl-2x': {'size': (2400, 1280), 'crop': 'scale', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin: Inner Container Background

        'content-plugin-inner-bg-xs': {'size': (320, get_height_from_ratio(450,4,3)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-xs-2x': {'size': (640, get_height_from_ratio(640,4,3)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-sm': {'size': (512, get_height_from_ratio(512,4,3)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-sm-2x': {'size': (1024, get_height_from_ratio(1024,4,3)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-md': {'size': (1030, get_height_from_ratio(1030,2,1)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-md-2x': {'size': (2060, get_height_from_ratio(2060,2,1)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-lg': {'size': (1200, get_height_from_ratio(1200,2,1)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-lg-2x': {'size': (2400, get_height_from_ratio(2400,2,1)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-xl': {'size': (1600, get_height_from_ratio(1600,2,1)), 'crop': 'scale', 'upscale': True },
        'content-plugin-inner-bg-xl-2x': {'size': (2400, get_height_from_ratio(2400,2,1)), 'crop': 'scale', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # App Content Plugin:

        # 1/1 (same as "Content Plugin" 3/3)
        'col-1-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-sm': {'size': (1200, get_height_from_ratio(1200,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-sm-2x': {'size': (1800, get_height_from_ratio(1800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-xl': {'size': (1500, get_height_from_ratio(1500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-xl-2x': {'size': (2500, get_height_from_ratio(2500,4,3)), 'crop': 'smart', 'upscale': True },

        # 1/2 (same as "Content Plugin" 1/2)
        'col-2-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-sm': {'size': (650, get_height_from_ratio(650,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-sm-2x': {'size': (900, get_height_from_ratio(900,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-xl': {'size': (800, get_height_from_ratio(800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-xl-2x': {'size': (1500, get_height_from_ratio(1500,4,3)), 'crop': 'smart', 'upscale': True },

        # 1/3 same as "Content Plugin" 1/3)
        'col-3-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-3-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-3-sm': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-3-sm-2x': {'size': (800, get_height_from_ratio(800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-3-xl': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-3-xl-2x': {'size': (1000, get_height_from_ratio(1000,4,3)), 'crop': 'smart', 'upscale': True },

        # 1/4
        'col-4-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-4-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-4-sm': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-4-sm-2x': {'size': (800, get_height_from_ratio(800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-4-xl': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-4-xl-2x': {'size': (1000, get_height_from_ratio(1000,4,3)), 'crop': 'smart', 'upscale': True },

        # 1/5
        'col-5-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-5-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-5-sm': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-5-sm-2x': {'size': (800, get_height_from_ratio(800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-5-xl': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-5-xl-2x': {'size': (1000, get_height_from_ratio(1000,4,3)), 'crop': 'smart', 'upscale': True },

        # 1/6
        'col-6-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-6-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-6-sm': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-6-sm-2x': {'size': (800, get_height_from_ratio(800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-6-xl': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-6-xl-2x': {'size': (1000, get_height_from_ratio(1000,4,3)), 'crop': 'smart', 'upscale': True },

        # Detail View
        'detail-full-width-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'detail-full-width-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'detail-full-width-sm': {'size': (1200, get_height_from_ratio(1200,4,3)), 'crop': 'smart', 'upscale': True },
        'detail-full-width-sm-2x': {'size': (1800, get_height_from_ratio(1800,4,3)), 'crop': 'smart', 'upscale': True },
        'detail-full-width-xl': {'size': (1500, get_height_from_ratio(1500,4,3)), 'crop': 'smart', 'upscale': True },
        'detail-full-width-xl-2x': {'size': (2500, get_height_from_ratio(2500,4,3)), 'crop': 'smart', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin:

        # 1/3 (same as "App Content Plugin" 1/3)
        'col-1-of-3-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-3-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-3-sm': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-3-sm-2x': {'size': (800, get_height_from_ratio(800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-3-xl': {'size': (500, get_height_from_ratio(500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-3-xl-2x': {'size': (1000, get_height_from_ratio(1000,4,3)), 'crop': 'smart', 'upscale': True },

        # 2/3
        'col-2-of-3-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-of-3-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-of-3-sm': {'size': (900, get_height_from_ratio(900,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-of-3-sm-2x': {'size': (1500, get_height_from_ratio(1500,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-of-3-xl': {'size': (1200, get_height_from_ratio(1200,4,3)), 'crop': 'smart', 'upscale': True },
        'col-2-of-3-xl-2x': {'size': (1800, get_height_from_ratio(1800,4,3)), 'crop': 'smart', 'upscale': True },

        # 3/3 (same as "App Content Plugin" 1/1)
        'col-3-of-3-xs': {'size': (450, get_height_from_ratio(450,2,1)), 'crop': 'smart', 'upscale': True },
        'col-3-of-3-xs-2x': {'size': (600, get_height_from_ratio(600,2,1)), 'crop': 'smart', 'upscale': True },
        'col-3-of-3-sm': {'size': (1200, get_height_from_ratio(1200,2,1)), 'crop': 'smart', 'upscale': True },
        'col-3-of-3-sm-2x': {'size': (1800, get_height_from_ratio(1800,2,1)), 'crop': 'smart', 'upscale': True },
        'col-3-of-3-xl': {'size': (1500, get_height_from_ratio(1500,2,1)), 'crop': 'smart', 'upscale': True },
        'col-3-of-3-xl-2x': {'size': (2500, get_height_from_ratio(2500,2,1)), 'crop': 'smart', 'upscale': True },

        # 1/2 (same as "App Content Plugin" 1/2)
        'col-1-of-2-xs': {'size': (450, get_height_from_ratio(450,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-2-xs-2x': {'size': (600, get_height_from_ratio(600,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-2-sm': {'size': (650, get_height_from_ratio(650,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-2-sm-2x': {'size': (900, get_height_from_ratio(900,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-2-xl': {'size': (800, get_height_from_ratio(800,4,3)), 'crop': 'smart', 'upscale': True },
        'col-1-of-2-xl-2x': {'size': (1500, get_height_from_ratio(1500,4,3)), 'crop': 'smart', 'upscale': True },

    },
}
