# -*- coding: utf-8 -*-
from allink_core.allink_base.utils import get_height_from_ratio

####################################################################################

# =Thumbnail Sizes (Responsive and Retina ready)

# Docs: http://easy-thumbnails.readthedocs.io/en/2.1/usage/#thumbnail-aliases

THUMBNAIL_ALIASES = {
    '': {

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin: video mobile image

        'video-mobile-image-xs': {'size': (320, 420), 'crop': 'smart'},
        'video-mobile-image-xs-2x': {'size': (500, 650), 'crop': 'smart'},
        'video-mobile-image-sm': {'size': (580, 760), 'crop': 'smart'},
        'video-mobile-image-sm-2x': {'size': (1000, 420), 'crop': 'smart'},

        # # # # # # # # # # # # # # # # # # # # # #
        # Content PLugin: In case html5 video is not supported, this fallback size has to do the job

        'video-poster-image': {'size': (1400, 800)}, # in case html5 video is not supported, this fallback size has to do the job

        # # # # # # # # # # # # # # # # # # # # # #
        # Slider (Swiper): INNER container slide background-image

        'slider-inner-container-xs': {'size': (320, 420)},
        'slider-inner-container-xs-2x': {'size': (640, 840), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-sm': {'size': (512, 560), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-sm-2x': {'size': (1024, 1120), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-md': {'size': (1030, 840), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-md-2x': {'size': (2060, 1280), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-lg': {'size': (1200, 840), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-lg-2x': {'size': (2400, 1280), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-xl': {'size': (1600, 1000), 'crop': 'smart', 'upscale': True },
        'slider-inner-container-xl-2x': {'size': (2400, 1280), 'crop': 'smart', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin: Parallax

        'parallax-xs': {'size': (320, 420)},
        'parallax-xs-2x': {'size': (640, 840), 'crop': 'scale'},
        'parallax-sm': {'size': (512, 560), 'crop': 'scale'},
        'parallax-sm-2x': {'size': (1024, 1120), 'crop': 'scale'},
        'parallax-md': {'size': (1030, 470), 'crop': 'scale'},
        'parallax-md-2x': {'size': (2060, 940), 'crop': 'scale'},
        'parallax-lg': {'size': (1200, 548), 'crop': 'scale'},
        'parallax-lg-2x': {'size': (2060, 940), 'crop': 'scale'},
        'parallax-xl': {'size': (1600, 730), 'crop': 'scale'},
        'parallax-xl-2x': {'size': (2400, 1100), 'crop': 'scale'},

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin: Full-Height Mode

        'full-height-xs': {'size': (320, 420)},
        'full-height-xs-2x': {'size': (640, 840), 'crop': 'smart', 'upscale': True },
        'full-height-sm': {'size': (512, 560), 'crop': 'smart', 'upscale': True },
        'full-height-sm-2x': {'size': (1024, 1120), 'crop': 'smart', 'upscale': True },
        'full-height-md': {'size': (1030, 840), 'crop': 'smart', 'upscale': True },
        'full-height-md-2x': {'size': (2060, 1280), 'crop': 'smart', 'upscale': True },
        'full-height-lg': {'size': (1200, 840), 'crop': 'smart', 'upscale': True },
        'full-height-lg-2x': {'size': (2400, 1280), 'crop': 'smart', 'upscale': True },
        'full-height-xl': {'size': (1600, 1000), 'crop': 'smart', 'upscale': True },
        'full-height-xl-2x': {'size': (2400, 1280), 'crop': 'smart', 'upscale': True },

        # # # # # # # # # # # # # # # # # # # # # #
        # Content Plugin: Inner Container Background

        'content-plugin-inner-bg-xs': {'size': (320, 420), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-xs-2x': {'size': (640, 840), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-sm': {'size': (512, 560), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-sm-2x': {'size': (1024, 1120), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-md': {'size': (1030, 840), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-md-2x': {'size': (2060, 1280), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-lg': {'size': (1200, 840), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-lg-2x': {'size': (2400, 1280), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-xl': {'size': (1600, 1000), 'crop': 'smart', 'upscale': True },
        'content-plugin-inner-bg-xl-2x': {'size': (2400, 1280), 'crop': 'smart', 'upscale': True },

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
