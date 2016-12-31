#! /usr/bin/env python
from setuptools import setup
from . import __version__ as version

setup(
    name='allink_core',
    version=version,
    description='collection of code fragments',
    long_description='collection of code fragments',
    author='Florian Türler, Beat Schenkel',
    author_email='itcrowd@allink.ch',
    url='http://github.com/allink/allink-core/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=[
        'allink_base',
        'allink_categories',
        'allink_styleguide',
        'djangocms_content',
        'djangocms_gallery',
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Communications :: Email',
    ],
    requires=[
    ],
    include_package_data=True,
)