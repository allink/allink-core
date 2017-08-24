# Installing allink-core

Add the following to your <code>requirements.in</code> file. And specify the version you want to use.

```
https://github.com/allink/allink-core/tarball/v1.0.0
```
Run:
```
./manage.py makemigrations
./manage.py migrate
```


# Upgrading allink-core
Whenever you want to upgrade allink-core it is helpful when you have the current state of your db from your live system. So you quickly see that all migrations run as expected.

Also make sure **before** update:
 - all your migrations in your have been applied
 - check the <code>CHANGELOG.md</code> espessially for parts in IMPORTANT (new requiremnts/ urls/ settings/ templates ..)


To update the core just set the tag or commit hash in <code>requirements.in</code>.
```
https://github.com/allink/allink-core/tarball/<<tag>> or <<commit hash>>
```

Make sure all the new requirements are installed:
```
divio project update
```

Run:
```
./manage.py makemigrations
./manage.py migrate
```


Also make sure **after** update:
 - let everybody in the team now that you updated the core. (otherwise they might accidentally create migrations to project specific apps (which depend on allink-core), with a older version of the core)


