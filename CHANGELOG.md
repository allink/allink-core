# Changelog


Each release is divided into the following main categories:

- IMPORTANT: These changes might not be backward compatible and require updating existing code. (If not applied correctly your update will fail)
    - SETTINGS: change your setting.py accordingly
    - TEMPLATES: if templates form allink_core are overridden, you have to double apply these changes
    - URLS: changes to urls.py
    - REQUIREMENTS: new or changed requirements
    - DATA MIGRATIONS: stuff to migrate by hand or create data migrations manually
- NEW: New features or plugins
- FIXES: General bugfixes


## v1.0.1 (under development)

### IMPORTANT

###### SETTINGS

- config_allink_page_toolbar_enabled is now definded in settings (definde in allink_settings):
```python
ALLINK_PAGE_TOOLBAR_ENABLED = False
```

- !! make sure CACHES and MIDDLEWARE settings is correct!!
-> every placeholder will be cached strictly!
-> if the project uses valid_from/ valid_to on e.g News or Events, this need a custom cache invalidation

use this a default:
```python
MIDDLEWARE_CLASSES = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debreach.middleware.RandomCommentMiddleware',
    'aldryn_django.middleware.RandomCommentExclusionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debreach.middleware.CSRFCryptMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'aldryn_sites.middleware.SiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lockdown.middleware.LockdownMiddleware',
    # 'allink_core.core.middleware.AllinkUrlRedirectMiddleware',
    'allink_core.core_apps.allink_legacy_redirect.middleware.AllinkLegacyRedirectMiddleware',
    # 'apps.country.middleware.DetectCountryMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'apps.product.middleware.DetectNeutralUrlsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
]

# ####################################################################################
#
# # Cache

# CACHE_MIDDLEWARE_KEY_PREFIX = 'winter'
#has no effect, unless the django caching middlewares are enabled
# http://djangocms.readthedocs.io/en/latest/how_to/caching/
# django.middleware.cache.UpdateCacheMiddleware
# django.middleware.cache.FetchFromCacheMiddleware


CMS_PAGE_CACHE = True
# only set following key, when CMS_PLACEHOLDER_CACHE is enabled as well:
# :17:cms-:1:1c526ad1bac1b1cce895c61f4a427529c672099d

CMS_PLACEHOLDER_CACHE = True
# sets all this keys
# :1:cms-|placeholder_cache_version|id:2|lang:de|site:1
# :1:cms-|render_placeholder|id:4|lang:de|site:1|tz:Europe/Zurich|v:1530043162304469

# CMS_PLUGIN_CACHE = True  # default is already True (this only sets this in every plugins as default)

CMS_CACHE_DURATIONS = {'content': 15552000, 'menus': 15552000, 'permissions': 15552000}

# CMS_CACHE_PREFIX = 'winter'  #default is 'cms'

PARLER_ENABLE_CACHING = False

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'django_dbcache',
#     }
# }

CACHE_TEMPLATE_FRAGMENT_LIFETIME = 15552000
CACHE_TEMPLATE_FRAGMENT_BACKEND = 'default'

# =Disable CACHING local
STAGE = senv('STAGE', 'local').lower()
if STAGE in {'local', 'test'}:
    CMS_PAGE_CACHE = False
    CMS_PLACEHOLDER_CACHE = False
    CMS_CACHE_DURATIONS = {
        'menus': 0,
        'content': 0,
        'permissions': 0,
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
        # 'default': {
        #     # 'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        #     # 'LOCATION': 'django_dbcache',
        #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #     'LOCATION': 'unique-snowflake',
        # },
        'locmem': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        },
        'db': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_dbcache',
        }
    }
    CACHE_TEMPLATE_FRAGMENT_LIFETIME = 15552000
    CACHE_TEMPLATE_FRAGMENT_BACKEND = 'default'

```


###### TEMPLATES

###### URLS

###### REQUIREMENTS

###### DATA MIGRATIONS

### NEW
- all manual caching stuff has been removed! (e.g events_preview_image, news_preview_image etc.)
- AllinkBaseModel djangocms placeholder cache invalidation on save
- THUMBNAIL_QUALITY = 60
- AllinkButton Plugin is now "cache = False"


### FIXES
- strip_anchor_part in LegacyRedirect on save



## v1.0.0

### IMPORTANT

###### SETTINGS

- Only register allink apps when actaully needed

```python
# allink apps which are installed in this project
INSTALLED_ALLINK_CORE_APPS = [
    'allink_core.apps.config',
    # 'allink_core.apps.contact',
    # 'allink_core.apps.events',
    # 'allink_core.apps.locations',
    # 'allink_core.apps.news',
    # 'allink_core.apps.members',
    # 'allink_core.apps.people',
    # 'allink_core.apps.testimonials',
    # 'allink_core.apps.work',
]
# allink apps which are overriden in this project
OVERRIDDEN_ALLINK_CORE_APPS = [
    # 'allink_apps.contact',
    # 'allink_apps.events',
    # 'allink_apps.locations',
    # 'allink_apps.news',
    # 'allink_apps.members',
    # 'allink_apps.people',
    # 'allink_apps.testimonials',
    # 'allink_apps.work',
]
INSTALLED_APPS.extend(get_core_apps(OVERRIDDEN_ALLINK_CORE_APPS, INSTALLED_ALLINK_CORE_APPS))

```

###### TEMPLATES

- Location Plugin Template: `details-and-map` has been renamed to `details_and_map` because of django naming conventions (underlines only), which should be the standard for future plugin template folders.

###### URLS

###### REQUIREMENTS

###### DATA MIGRATIONS

### NEW
- BooleanField is_active on AllinkBaseModel got changed to a IntegerField with choices named status.
- Added automatic ids to forms and ButtonLinkPlugin to make it easier to use google tag manager.
- Added option `manual_filtering` to `AllinkBaseAppContentPlugin`. Applies individual query filters to app queryset. Override in app instance (i.e. events) for custom filters. Implementation example:
    ```python
    class BaseEventsAppContentPlugin(AllinkBaseAppContentPlugin):

    ...

    # FILTERING
    DEFAULT = 'default'
    UPCOMING = 'upcoming'
    PAST = 'past'

    FILTERING = (
        (DEFAULT, '---------'),
        (UPCOMING, 'upcoming'),
        (PAST, 'past'),
    )

    def _apply_filtering_to_queryset_for_display(self, queryset):
        # upcoming
        if self.manual_filtering == BaseEventsAppContentPlugin.UPCOMING:
            return queryset.upcoming_entries()
        # past
        elif self.manual_filtering == BaseEventsAppContentPlugin.PAST:
            return queryset.past_entries()
        return queryset

    ...
    ```
- New Newsletter plugin with associated text fields in the config app. On mailchimp add the custom fields `GDPR_EMAIL` and `GDPR_ADS` to your list. Add `'allink_core.apps.newsletter',` to `INSTALLED_ALLINK_CORE_APPS` and `('newsletter:signup', _(u'Mailchimp Newsletter Signup')),` to `BUTTON_LINK_SPECIAL_LINKS_CHOICES` to use it in your project.

### FIXES
- Added striptags in `allink_seo_tags.py` to model field `lead`, because it can contain html.
- Replace `countries` field with `country` in locations admin
