# Changelog

Each release is divided into the following main categories:

- IMPORTANT: These changes might not be backward compatible and require updating existing code. (If not applied correctly your update will fail)
    - SETTINGS: change your setting.py accordingly
    - TEMPLATES: if templates form allink_core are overriden, you have to double apply these changes
    - URLS: changes to urls.py
    - REQUIREMENTS: new or changed requirements
    - DATA MIGRATIONS: stuff to migrate by hand or create data migrations manually
- NEW: New features or plugins
- FIXES: General bugfixes

## v1.0.0

### IMPORTANT


###### SETTINGS
- PROJECT_COLORS is now a tuple and not a list anymore

###### TEMPLATES
- new templates:
   - admin/submit_line.html
   - admin/change_form.html
   - accounts/...
- modificaton in base_root.html (new tag favicons)


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
