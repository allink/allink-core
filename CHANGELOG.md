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


## v1.0.0 (under development)

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
OVERIDDEN_ALLINK_CORE_APPS = [
    # 'allink_apps.contact',
    # 'allink_apps.events',
    # 'allink_apps.locations',
    # 'allink_apps.news',
    # 'allink_apps.members',
    # 'allink_apps.people',
    # 'allink_apps.testimonials',
    # 'allink_apps.work',
]

```

###### TEMPLATES

###### URLS

###### REQUIREMENTS

###### DATA MIGRATIONS

### NEW
- BooleanField is_active on AllinkBaseModel got changed to a IntegerField with choices named status.

### FIXES
