import os.path  # noqa
from collections import OrderedDict  # noqa
from allink_core.core.allink_settings import *  # noqa
from allink_core import get_core_apps, ALLINK_CORE_MAIN_TEMPLATE_DIRS
from django.utils.translation import ugettext_lazy as _

####################################################################################

# Test Settings

print('=========================')  # noqa
print('In TEST Mode - Disableling Migrations')  # noqa
print('=========================')  # noqa


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

####################################################################################

# addon: aldryn-django
# PREFIX_DEFAULT_LANGUAGE = True -> sets 'aldryn_django.middleware.LanguagePrefixFallbackMiddleware'
# MIGRATION_COMMANDS ->
BASE_DIR = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['localhost', '*']
SITE_ID = 1
# WSGI_APPLICATION = 'wsgi.application'
ROOT_URLCONF = 'test.urls'

SECRET_KEY = 'not-very-random'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATICFILES_STORAGE = 'aldryn_django.storage.GZippedStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TIME_ZONE = 'Europe/Zurich'

USE_L10N = True
USE_I18N = True

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    ('fr', 'French'),
)

CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': 'English',
            'fallbacks': ['de', 'fr', ]
        },
        {
            'code': 'de',
            'name': 'Deutsche',
            'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'fr' HERE
        },
        {
            'code': 'fr',
            'name': 'Française',
            'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'de' HERE
        },
        {
            'code': 'it',
            'name': 'Italiano',
            'fallbacks': ['fr', ]  # FOR TESTING, LEAVE AS ONLY 'fr'
        },
    ],
    'default': {
        'redirect_on_fallback': True,  # PLEASE DO NOT CHANGE THIS
    }
}

PARLER_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'fallbacks': ['de', ],
        },
        {
            'code': 'de',
            'fallbacks': ['en', ],
        },
    ],
    'default': {
        'code': 'en',
        'fallbacks': ['en'],
        'hide_untranslated': False
    }
}

# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, 'locale'),
# ]

DATABASES = {
    'default': {
        'NAME': 'db',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'OPTIONS': {},
        'TIME_ZONE': None,
        'TEST': {'CHARSET': None, 'COLLATION': None, 'NAME': None, 'MIRROR': None}
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/app/templates', '/app/allink_core/core/templates/allink_core'].extend(ALLINK_CORE_MAIN_TEMPLATE_DIRS),
        'OPTIONS':
            {'debug': True,
             'context_processors': [
                 'django.contrib.auth.context_processors.auth',
                 'django.contrib.messages.context_processors.messages',
                 'django.template.context_processors.i18n',
                 'django.template.context_processors.debug',
                 'django.template.context_processors.request',
                 'django.template.context_processors.media',
                 'django.template.context_processors.csrf',
                 'django.template.context_processors.tz',
                 'django.template.context_processors.static',
                 # 'aldryn_django.context_processors.debug',
                 'sekizai.context_processors.sekizai',
                 'cms.context_processors.cms_settings',
                 # 'aldryn_boilerplates.context_processors.boilerplate',
                 # 'aldryn_snake.template_api.template_processor',
                 'django.template.context_processors.request'
             ],
             'loaders': [
                 'django.template.loaders.filesystem.Loader',
                 # 'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
                 'django.template.loaders.app_directories.Loader'
             ]
             }
    }
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    # 'aldryn_sites.middleware.SiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'lockdown.middleware.LockdownMiddleware',
    # 'allink_core.core.middleware.AllinkUrlRedirectMiddleware',
    'allink_core.core_apps.allink_legacy_redirect.middleware.AllinkLegacyRedirectMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
]

####################################################################################

# Caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

####################################################################################

# Installed Apps

INSTALLED_APPS = [
    # 'aldryn_addons',
    # 'aldryn_django',
    # 'aldryn_sso',
    # 'aldryn_django_cms',
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'parler',
    'robots',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'mptt',
    'aldryn_common',
    'aldryn_google_tag_manager',
] + ALLINK_INSTALLED_APPS

# project specific apps
PROJECT_APPS = [

]

INSTALLED_APPS.extend(PROJECT_APPS)

# allink apps which are installed in this project
INSTALLED_ALLINK_CORE_APPS = [
    'allink_core.apps.config',
    # 'allink_core.apps.contact',
    # 'allink_core.apps.events',
    # 'allink_core.apps.locations',
    'allink_core.apps.news',
    # 'allink_core.apps.people',
    # 'allink_core.apps.testimonials',
]
# allink apps which are overriden in this project
OVERRIDDEN_ALLINK_CORE_APPS = [
    # 'allink_apps.contact',
    # 'allink_apps.events',
    # 'allink_apps.locations',
    # 'allink_apps.news',
    # 'allink_apps.people',
    # 'allink_apps.testimonials',
]
INSTALLED_APPS.extend(get_core_apps(OVERRIDDEN_ALLINK_CORE_APPS, INSTALLED_ALLINK_CORE_APPS))

####################################################################################

# Locale paths
LOCALE_PATHS = ALLINK_LOCALE_PATHS

####################################################################################

# django CMS
CMS_PERMISSION = True
CMS_TEMPLATES = (
    ('default.html', 'Default'),
    ('404.html', '404 - Page not found'),
)

####################################################################################

#  allink categories
# all models which use categories have to be listed here.
# the value has to be equal to "_meta.model_name"
# -> Overeride if project specific setup requires

PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES = ALLINK_PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES
PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES.extend([
    # ('locations', 'Locations'),
])

# auto generate categories, when an item form this app is saved.
# all models which can be used as tag for categories.
# all categories with the same tag can be used
# in a filter on a plugin.
# the value has to be equal to "_meta.model_name"

PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES = [
    # ('locations', 'Locations'),
]

# used to display category names on app models
# (e.g. units on People App)
# ATTENTION!! Changing the keys requires data migrations!
PROJECT_CATEGORY_IDENTIFIERS = (
    ('units', 'Unit'),
)

PROJECT_LINK_APPHOOKS = OrderedDict([
    ('Page', []),  # Not Apphook but linkable
    # ('NewsApphook', {'detail': ('allink_core.apps.news.models.News', ['slug'])}),
    # ('EventsApphook', {'detail': ('allink_core.apps.events.models.Events', ['slug'])}),
    # ('LocationsApphook', {'detail': ('allink_core.apps.locations.models.Locations', ['slug'])}),
    # ('PeopleApphook', {'detail': ('allink_core.apps.people.models.People', ['slug'])}),
    # ('TestimonialsApphook', {'detail': ('allink_core.apps.testimonials.models.Testimonials', ['slug'])}),
])

####################################################################################
#  =project colors

# use Hex values with 6 letters/ define in lowercase
# ATTENTION!! Changing the keys requires data migrations!
PROJECT_COLORS = {
    # '#000000': 'project-color-1',  # black
}

####################################################################################

# allink app_content additional templates for apps
# ATTENTION!! Changing the keys requires data migrations!
# the variable name prefix 'PEOPLE' in 'PEOPLE_PLUGIN_TEMPLATES' has to be equal to "_meta.model_name"
# default templates are (these exist as templates in core dir):
#     ('grid_static', 'Grid (Static)'),
#     ('grid_dynamic', 'Grid (Dynamic)'),
#     ('list', 'List'),
#     ('slider', 'Slider'),
#     ('table', 'Table'),

NEWS_PLUGIN_TEMPLATES = (
    ('grid_static', 'Grid (Static)'),
)

EVENTS_PLUGIN_TEMPLATES = (
    ('grid_static', 'Grid (Static)'),
)

LOCATIONS_PLUGIN_TEMPLATES = (
    ('map', 'Map'),
    ('details', 'Details'),
    ('details-and-map', 'Details and Map'),
)

PEOPLE_PLUGIN_TEMPLATES = (
    ('grid_static', 'Grid (Static)'),
)

TESTIMONIALS_PLUGIN_TEMPLATES = (
    ('slider', 'Slider'),
)

####################################################################################
#  =other templates which are defined in settings


TEASER_PLUGIN_TEMPLATES = (
    ('default', 'Default'),
)
TEASER_PAGE_LINK_TEXT = _('Read more')

GALLERY_PLUGIN_TEMPLATES = (
    ('slider', 'Slider'),
)

INSTAGRAM_PLUGIN_TEMPLATES = (
    ('grid_static', 'Grid (Static)'),
)

ADDITIONAL_CONTENT_PLUGIN_TEMPLATES = (
    # ('col-3-variation', '3 Columns (footer)', 3, 'col-1-of-3'),
)

ADDITIONAL_NEWS_DETAIL_TEMPLATES = (
    # ('with_header', 'With lead section'),
)
ADDITIONAL_EVENTS_DETAIL_TEMPLATES = (
    # ('with_header', 'With lead section'),
)

####################################################################################
# css classes
# each plugin has its own set (except all form plugins share FORM_CSS_CLASSES)
# ATTENTION!! Changing the keys requires data migrations!

# CONTENT_CSS_CLASSES = ()
# FORM_CSS_CLASSES = ()
# BUTTON_LINK_CSS_CLASSES = ()
# ICON_CSS_CLASSES = ()
# IMAGE_CSS_CLASSES = ()
# LOCATIONS_CSS_CLASSES = ()
# GALLERY_CSS_CLASSES = ()
# VID_EMBED_CSS_CLASSES = ()
# VID_FILE_CSS_CLASSES = ()
SOCIAL_ICON_CSS_CLASSES = (
    # ('footer-icons', 'Icons in page footer.'),
)

# BLOG_CSS_CLASSES = ()
# LOCATIONS_CSS_CLASSES = ()
# PEOPLE_CSS_CLASSES = ()
# TESTIMONIALS_CSS_CLASSES = ()
# ...

CONTENT_CSS_CLASSES = (
    ('hidden-on-desktop', 'Visibility: Hide this content section on DESKTOP devices.'),
    ('hidden-on-mobile', 'Visibility: Hide this content section on MOBILE devices.'),
    ('spacings-disabled',
     'Spacing: Remove any spacing (margin and padding) of this section (still keeps spacings from other sections).'),
)

BUTTON_LINK_CSS_CLASSES = (
    # ('secondary-nav', 'Secondary Navigation'),
)

####################################################################################

# SOCIAL ICONS
# Used in the 'Social Icon' plugin
# Important: These keys have to match the map defined in the CSS variables
# ATTENTION!! Changing the keys requires data migrations!

FACEBOOK = 'facebook'
INSTAGRAM = 'instagram'
PINTEREST = 'pinterest'
TWITTER = 'twitter'
SNAPCHAT = 'snapchat'
SPOTIFY = 'spotify'
LINKEDIN = 'linkedin'
XING = 'xing'
YOUTUBE = 'youtube'
VIMEO = 'vimeo'
GOOGLEPLUS = 'googleplus'
TRIPADVISOR = 'tripadvisor'
KUNUNU = 'kununu'

SOCIAL_ICONS_CHOICES = (
    (FACEBOOK, 'Facebook'),
    (INSTAGRAM, 'Instagram'),
    # (PINTEREST, 'Pinterest'),
    # (TWITTER, 'Twitter'),
    # (SNAPCHAT, 'Snapchat'),
    # (LINKEDIN, 'Linkedin'),
    # (SPOTIFY, 'Spotify'),
    # (XING, 'Xing'),
    # (YOUTUBE, 'Youtube'),
    # (VIMEO, 'Vimeo'),
    # (GOOGLEPLUS, _ Plus'),
    # (TRIPADVISOR, 'TripAdvisor'),
    # (KUNUNU, 'kununu'),
)

####################################################################################

# CMSAllinkContentPlugin

ALLINK_CONTENT_PLUGIN_CHILD_CLASSES = \
    ALLINK_CONTENT_PLUGIN_CHILD_CLASSES + [
    ]

# ATTENTION!! Changing the keys requires data migrations!
CONTENT_TITLE_CHOICES = (
    # ('h1', 'Title Large'),
    ('h2', 'Title Medium'),
    ('h3', 'Title Small'),
)
CONTENT_TITLE_CHOICES_DEFAULT = 'h2'

# ATTENTION!! Changing the keys requires data migrations! (Never change 'default'!)
CONTENT_ON_SCREEN_EFFECT_CHOICES = (
    ('default', 'Default'),
)
####################################################################################

# CMSAllinkGroupPlugin

CMS_ALLINK_GROUP_PLUGIN_CHILD_CLASSES = (
    # 'TextPlugin',
    # 'CMSAllinkImagePlugin',
    'CMSAllinkButtonLinkContainerPlugin',
    'CMSAllinkButtonLinkPlugin',
)
####################################################################################

# CMSAllinkButtonLinkPlugin

BUTTON_LINK_SPECIAL_LINKS_CHOICES = (
    # ('some_view', 'Some View Name'),
)

####################################################################################

# Thumbnail width aliases

THUMBNAIL_WIDTH_ALIASES = {
    # used for plugins e.g. image, gallery>image
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
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': False,
        'BUNDLE_DIR_NAME': 'webpack_bundles/', # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}