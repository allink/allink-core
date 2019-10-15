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
        'DIRS': ['/app/templates', '/app/allink_core/core/templates/allink_core'],
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
# add allink-core templates
dirs = TEMPLATES[0].get('DIRS', {})
dirs.extend(ALLINK_CORE_MAIN_TEMPLATE_DIRS)

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
)

####################################################################################

# allink categories
# all models which use categories have to be listed here.
# the value has to be equal to "_meta.model_name"
# -> Overeride if project specific setup requires

PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES = ALLINK_PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES
PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES.extend([
    # ('locations', 'Locations'),
])

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

####################################################################################
#  Teaser

TEASER_PAGE_LINK_TEXT = _('Read more')

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