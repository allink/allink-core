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







## v1.1.0 (under development)

### IMPORTANT

###### SETTINGS
- you must set ALLINK_MANDRILL_DEV_MODE=True on development and all stage environments! (please also set ALLINK_MANDRILL_DEV_MODE=False on production in the environment variables)

###### TEMPLATES
- we removed the context variable 'form_name' and moved the information to the button_link_plugin -> 'instance.unique_identifier'. if you have overridden allink_button_link/item.html you need to rename it.
- to boost rendering of GalleryPlugins you can replace "ratio=instance.get_parent.get_plugin_instance.0.ratio" with "ratio=instance.ratio" in your gallery templates
- if you have overriden any core form template (an ajax-form) with a {% csrf_token %} (most likely one of these: allink_mailchimp/signup_form_advanced_base.html or allink_mailchimp/signup_form_base.html) you need to remove the {% csrf_token %}.

###### URLS
- you need to add:
```python
url(r'^cms-api/', include('allink_core.core_apps.allink_cms.urls', namespace='cms_api')),
```
###### REQUIREMENTS
- djangorestframework==3.7.0

###### DATA MIGRATIONS

### NEW
- we now save the data of the content-plugin to these plugins directly 'AllinkImagePlugin', 'AllinkGalleryPlugin', 'AllinkGalleryImagePlugin'
- (allink-core-static dependent!) all forms with class "ajax-form" now get sent with the appropriate csrftoken which will be fetched from the cookie. you don't need a {% csrf_token %} in the template (this is why we can now cache CMSAllinkSignupFormPlugin and any other CMSPlugin displaying a form) -> if you decide to change cache=False to cache=True you must remove {% csrf_token %} from the template and clear cache! otherwise you will end up with a 403!
- we added a basic way to load plugins async. just add a template:
../content_skeleton.html
```html
{% load cms_tags %}
<div class="plugin--tpl-skeleton" data-rendered-plugin-url="{% url 'cms_api:plugins' id=instance.cmsplugin_ptr_id %}"></div>
```
and add the following to your Plugin in cms_plugins.py:
```python
    ...
    def get_render_template(self, context, instance, placeholder):
        if context['request'].is_ajax() or context['request'].toolbar.edit_mode:
            return '<<path to template>>/content.html'
        else:
            return '<<path to template>>/content_skeleton.html'
    ...
``

### FIXES

## v1.0.2

### IMPORTANT
- all plugin models inherit from AllinkBaseAppContentPlugin now have a field 'apphook_page'. Especially the ones created in the project itself (by new_app or fork_app)now have to be updated as well. Otherwise the plugins will fail when edited, because the Field was not added.
for example:
```python
class ServicesAppContentPlugin(AllinkBaseAppContentPlugin):
    ...
    apphook_page = PageField(
        verbose_name=_(u'Apphook Page'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_(u'If provided, this Apphook-Page will be used to generate the detail link.'),
    )
```


###### SETTINGS

###### TEMPLATES

###### URLS

###### REQUIREMENTS

###### DATA MIGRATIONS

### NEW
- new templatetag 'get_absolute_url'. Use {% get_absolute_url object instance.apphook_page.application_namespace %} in a plugin template if you specified a different apphook than the default.

### FIXES
- Set new cache of Config app after save


## v1.0.1

### IMPORTANT

- if you have custom plugins in this project, make sure:
    1. that the model you display inherits from 'AllinkInvalidatePlaceholderCacheMixin'.
    2. that you define an attribute 'data_model' on the Plugin
- make sure all plugins with forms have cache=False, otherwise CRSF token gets cached too. [more information](:https://github.com/divio/django-cms/issues/4330)


###### SETTINGS

- config_allink_page_toolbar_enabled is now definded in settings (definde in allink_settings):
```python
ALLINK_PAGE_TOOLBAR_ENABLED = False
```

- every cms placeholder will be cached strictly!

manual updates in all projects:
- make sure CACHES and MIDDLEWARE settings is correct!! (see default settings below)
- make sure to delete django_dbcache manually on production as there are a lot of stale cache entries
- make sure to delete all template caches in the overwritten templates (search for "{% cache") (also remove the imports)
- run the cache warmer (for the moment locally). You just have to feed it with the sitemap.xml. You find an example [here.](https://gist.github.com/tuerlefl/028f338b63e6d951601d96b567b2bdd0)

special cases:
- if the project uses valid_from/ valid_to on e.g News or Events, this need a custom cache invalidation
- in projects where the cache backend is "UWSGI_CACHE" make sure, you remove the env variables "UWSGI_CACHE2" and "CACHE_URL" from production/ stage

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


CMS_PAGE_CACHE = False
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

# this is default on divio cloud anyway
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'django_dbcache',
#     }
# }

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
    }

```


###### TEMPLATES

###### URLS

###### REQUIREMENTS

###### DATA MIGRATIONS

### NEW
- all manual caching stuff has been removed! (e.g events_preview_image, news_preview_image etc.)
- AllinkBaseModel djangocms placeholder cache invalidation on save
- AllinkButton Plugin is now "cache = False"
- AllinkBaseDetailView: optional app detail template override for each app category (naming convention: `<app_name>_<category_slug>_detail.html`)


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
