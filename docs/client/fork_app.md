# Forking an app

The following guide explains how you can override an app from allink-core/apps.

We provided you with a management command <code>fork_app</code>.

The Following command will create a new module called <code>work</code> inside the directory <code>apps/</code>
```
./manage.py fork_app work apps
```


!!! note
    It would be possible to fork an app in every directory you want. However to keep a certain structure in all our projects we always create a directory <code>apps</code>.


The console will output the steps needed to complete the process.
```
The final step is uncomment "new_app.config" in OVERRIDDED_ALLINK_CORE_APPS (replacing
the equivalent allink_core app). e.g.:

    # settings.py
    ...

    OVERRIDDEN_ALLINK_CORE_APPS = [
        # 'apps.contact',
        # 'apps.events',
        # 'apps.locations',
        # 'apps.news',
        # 'apps.members',
        # 'apps.people',
        # 'apps.testimonials',
        # 'apps.work',
    ]
```

The files which have been created just provide you with the minimal file structure. But you are now ready to override and extend what ever you want.


For a some more guidance use the management command <code>fork_app_help</code>. This provides you with some usefull comments in every file.
```
./manage.py fork_app_help work apps
```