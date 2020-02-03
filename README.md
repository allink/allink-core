# allink-core
allink-core is a heavily opinionated collection of django apps, django-cms plugins and other utilities. allink-core was implemented to create a standardized ecosystem for django-cms projects developed at [allink AG](https://www.allink.ch).

allink-core is ment to be used with our boilerplate project which is hosted on the [divio cloud](https://www.divio.com/en/). (feel free to send us a [message](mailto:itcrowd@allink.ch) if you would like to have a look.)
The steps we describe here are mostly closely coupled to our setup and environment. So the described steps might not make sense to you, when you don't know our setup. Also we skip steps which we already included in the boilerplate.

## Documentation
[v2.x.x](http://allink-core.readthedocs.io/en/v2.x.x/)

## Working on documentation
`make docs` will serve you a preview of the local docs on "http://127.0.0.1:8000". More Information on [mkdocs.org](http://www.mkdocs.org/) or [mkdocs rtd](https://mkdocs.readthedocs.io/en/stable/).

## Release conventions

### Major
v.0.x.x, v.1.x.x and v.2.x.x are not compatible with each other. We never migrated from one to an other and doing so would be a be a lot of manual work, as there have been a lot of database changes. We try to minimize the need for a new major version. The decision if v3.x.x will be compatible with v.2.x.x has yet to be made.

### Minor
When you make changes that affect both the [backend](https://github.com/allink/allink-core) and the [frontend](https://github.com/allink/allink-core-static) the project dependencies need to be updated at the same time. To quickly see which releases belong together you should make a `minor` release in both repositories.

#### Example
A new CMS plugin together with styles has been added to the core. Release a new `minor` version:

- `allink-core==v2.3.0`
- `allink-core-static@v2.3.0`

### Patch
Changes that only affect a single repo should be tagged with a `patch` release. Usually needed for small adjustments and bugfixes.

#### Example
A bugfix has been made in allink-core. Release a new `patch` version:

- `allink-core==v2.3.2`

## Workflow when making updates to allink-core repo while working on a project.
The idea is that we want to be able to make changes to the allink-core repo with real life data. This can be achieved, when we are able to switch out the installed allink-core form the requirements.in with a local allink-core repo. This way we can also maintain a proper git history.

### Prepare allink-core repository
To work on the allink-core repo you first need to pull the [allink-core](https://github.com/allink/allink-core) repo. The setup expects it to be at "~/projects/allink-core". If it isn't in this location, just create a symlink which points to your allink-core repo.

1. make sure you are up to date with the current version branch e.g "v2.0.x" and you working on your own branch.
2. create a virtualenv `virtualenv env`
3. install requirements `pip install -r requiremnts_dev.txt`

For the next steps, we assume you are working on the [boilerplate-2.0](https://github.com/allink/boilerplate-2.0) project, but this should work with every project which follows the same principles and have allink-core installed.

### Prepare boilerplate-2.0 repository
1. To override the already installed allink-core requirements, we have to mount the local allink-core directory as a volume into the docker container. Add `- "~/projects/allink-core/allink_core:/app/allink_core:rw"` to the docker-compose.yml file.
2. To work directly on allink-core in the same directory as the boilerplate-project, we create a symlink. `ln -s ~/projects/allink-core/allink_core allink_core`

> Make sure you do not commit these changes, as your teammates probably do not care about having a local allink-core mapped in their project.

> Make added or updated translations with the following command: `./manage.py makemessages --symlinks`

You are all set. When you now run `docker-compose up` your application will run with your local allink-core repo. However if you run `docker-compose build` you will still be installing the allink-core repo from the requirements file.

If you need to run `docker-compose build` with your new branch. Just commit your changes to your feature branch on the allink-core repo and add it to the boilerplate-2.0 requirementsfile with the corresponding commit hash. e.g: `https://github.com/allink/allink-core/tarball/ccb67deaed7dbc07bd565c717a21c0a07752bd9d`

### create a new release of allink-core
1. create a new pull request (make sure you include your changes to CHANGELOG.md)
2. merge back to version branch e.g v2.0.x
3. `make patch` or `make minor` depending on what version you want to create. (this will create a new commit and push the new tags to github) If you need an other version do it with `bumpversion`.
4. create a new release on PyPi `make release` (make sure you have the correct credentials for allink in your [~/.pypirc](https://docs.python.org/3.3/distutils/packageindex.html#the-pypirc-file) also for [test-pypi](https://packaging.python.org/guides/using-testpypi/#setting-up-testpypi-in-pypirc))
