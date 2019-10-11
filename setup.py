#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
from setuptools import setup, find_packages


def get_version(*file_paths):
    """Retrieves the version from allink_core/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("allink_core", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    sys.exit()

readme = open('README.md').read()

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 2.0',
    'Framework :: Django :: 2.1',
    'Framework :: Django :: 2.2',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

INSTALL_REQUIREMENTS = [
    'Django>=2.0,<3.0',
]

setup(
    name='allink-core',
    version=version,
    description='A collection of apps used in allink cms-projects.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='allink AG and contributors',
    author_email='itcrowd@allink.ch',
    url='http://github.com/allink/allink-core/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(exclude=['tests', 'tests.*', ]),
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
)
