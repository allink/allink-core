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



## v0.0.7

### IMPORTANT

###### SETTINGS
- contacts migration folder was added to allink_settings, so you have to create a folder `contacts` (and create an empty `__init__.py` in it [ha!]) within `apps/allink_apps_migrations`. If you already have migrated contacts you have to manually copy all migrations to the app specific folder.
- new setting PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES must be added by core update.
```python
# all models which can be used as tag for categories.
# all categories with the same tag can be used
# in a filter on a plugin.
# the value has to be equal to "_meta.model_name"
PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES = [
    ('locations', 'Locations'),
]
```

###### TEMPLATES

###### URLS

###### REQUIREMENTS

###### DATA MIGRATIONS

### NEW
- allink_apps: galleries not on app anymore, instead the gallery on detail page is added with GalleryPlugin
- Plugin overview pages can be filterd over dropdowns by Foreingkey- and Char-Fields
    - Hint for updates: keyword argument "filter" in methode "get_render_queryset_for_display" on BlogAppContentPlugin must be renamed to "filters"
- allink_categories: model_categories can be defined on child and/or parent.
- allink_categories: categories can get generated from other apps, an get a tag. Like this when using an ajax filter by category, only categories generated from a specific model can be choosen.
- allink_apps: App Plugins now support AND operator for filtering categories
- allink_apps: get_absolute_urlallow now language as parameter

### FIXES
- Bugfix in djangocms_instagram: Added queryset length when no display option with paginated_by value
- Content Plugin: The template `content.html` can now be overwritten on a project basis with the following required content `{% extends "djangocms_content/content_base.html" %}`. Afterwards blocks can be set.


## v0.0.6

### IMPORTANT

###### SETTINGS
- PROJECT_COLORS is now a tuple and not a list anymore
- CMS_PLACEHOLDER_CONF was supplemented with the placeholder fields from allink_apps
- members migration folder was added to allink_settings, so you have to create a folder (with "__init__.py") in apps/allink_apps_migrations.

###### TEMPLATES
- new templates:
   - admin/submit_line.html
   - admin/change_form.html
   - accounts/...
- modificaton in base_root.html (new tag favicons)
- modification in every plugin template form allink_apps 'object.show_detail_link' introduced.
- allink_config: base_title and og_image in base_root.html


###### URLS
- debug_toolbar urls added
- contact urls added

###### REQUIREMENTS
- new
    - django-polymorphic==0.8.1
    - django-debug-toolbar==1.7

###### DATA MIGRATIONS
- allink_legacy_redirect has to be manually migrated because migration '0006_auto_20170320_0702' was not working correctly.
- blog: datamigrations blog polymorphic (see data migrations as reference [file](https://www.google.com))
- blog: detail placeholderfield datamigrations
- djangocms_image: (danach djangocms_picture delete table contents and uninstall

### NEW

- Instagram Plugin: Initial release
- Content Plugin: Utility blocks added to default `content.html` that now can be extended on a project basis.
- Content Plugin: Empty columns now get the class `col-empty` and are set to `display:none;` by default on mobile devices.
- Content Plugin: Support for column ordering (for mobile only) has been added. Requires the latest `allink-core-static`.
- Allink Legacy Redirects: Redirects for legacy URLs with GET parameters consider the parameters.

### FIXES

- Button/Link Plugin: CSS classes are now set.
- Button/Link Plugin: Admin modal: Link settings are now expanded per default.
- Button/Link Plugin: `get_link_special_choices` has now a blank default value.
