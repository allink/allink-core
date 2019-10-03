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

## v2.0.2
### IMPORTANT
###### SETTINGS
###### TEMPLATES
###### URLS
###### REQUIREMENTS
###### DATA MIGRATIONS
### NEW
- removed TransactionTestCase and CMSTransactionTestCase where not needed
- removed filter_fields from appcontent plugin
- removed filters param from get_render_queryset_for_display
- moved select manual entries to get_render_queryset_for_display
### FIXES

## v2.0.1
### IMPORTANT
###### SETTINGS
###### TEMPLATES
###### URLS
###### REQUIREMENTS
###### DATA MIGRATIONS
### NEW
- admin and plugins are no longer translated, we removed every translated string from the admin. This should make translation of the customer specific frontend relevant fields easier.
- The favicon set is now added with an include rather than rendered with a templatetag.
### FIXES