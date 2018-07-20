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
