import os.path
import tempfile
from allink_core.core.allink_settings import *  # noqa
from allink_core import get_core_apps, ALLINK_CORE_MAIN_TEMPLATE_DIRS
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.abspath(__file__))))
TEST_DIR = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))

SITE_ID = 1
ROOT_URLCONF = 'test.urls'
STAGE = 'local'

SECRET_KEY = 'not-very-random'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = tempfile.TemporaryDirectory(prefix='media_test').name
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
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'allink_core/core/templates/allink_core/')],
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

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
    'mptt'] + ALLINK_INSTALLED_APPS

# allink apps which are installed in this project
INSTALLED_ALLINK_CORE_APPS = [
    'allink_core.apps.config',
    # 'allink_core.apps.locations',
    'allink_core.apps.news',
    # 'allink_core.apps.people',
    # 'allink_core.apps.testimonials',
]
# allink apps which are overriden in this project
OVERRIDDEN_ALLINK_CORE_APPS = [
    # 'allink_apps.locations',
    # 'allink_apps.news',
    # 'allink_apps.people',
    # 'allink_apps.testimonials',
]
INSTALLED_APPS.extend(get_core_apps(OVERRIDDEN_ALLINK_CORE_APPS, INSTALLED_ALLINK_CORE_APPS))

LOCALE_PATHS = ALLINK_LOCALE_PATHS

CMS_PERMISSION = True
CMS_TEMPLATES = (
    ('default.html', 'Default'),
)

PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES = ALLINK_PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES

NEWS_PLUGIN_TEMPLATES = (
    ('grid_static', 'Grid (Static)'),
)

TEASER_PAGE_LINK_TEXT = _('Read more')

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
    'test-original': {
        'xs': {'width': 450, 'ratio': 'x-y'},
        'sm': {'width': 500, 'ratio': 'x-y'},
        'xl': {'width': 500, 'ratio': 'x-y'}
    },
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': False,
        'BUNDLE_DIR_NAME': 'webpack_bundles/',  # must end with slash
        'STATS_FILE': os.path.join(TEST_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

SOLO_CACHE_TIMEOUT = 60 * 60 * 24 * 180