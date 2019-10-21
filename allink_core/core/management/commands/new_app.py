# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError
from django.utils import six

from allink_core.core.customisation.utils import create_new_app


class Command(BaseCommand):
    help = ("Create a new app with some allink boilerplate code.")

    def add_arguments(self, parser):
        parser.add_argument(
            'dummy_app_path',
            help='The path to copy the files to',
            nargs='?',
            default='allink_core/core/customisation/dummy_new_app'
        )
        parser.add_argument('app_label', help='The application name')
        parser.add_argument('model_name', help='The model name')
        parser.add_argument('app_path', help='The path to copy the files to', nargs='?', default='apps')

    def handle(self, *args, **options):

        dummy_app_path = options['dummy_app_path']
        app_label = options['app_label']
        model_name = options['model_name']
        app_path = options['app_path']

        try:
            create_new_app(
                dummy_app_path=dummy_app_path,
                app_label=app_label,
                app_path=app_path,
                model_name=model_name
            )
        except Exception as e:
            raise CommandError(six.text_type(e))

        msg = (
            """
                The final steps:\n
                1. add '{app_path}.{app_label}', to PROJECT_APPS \n
                2. add 'CMS{model_name}AppContentPlugin', Plugins to ALLINK_CONTENT_PLUGIN_CHILD_CLASSES \n
                3. add ('{model_name}Apphook', {{'detail': ('apps.{app_label}.models.{model_name}', ['slug'])}}), to PROJECT_LINK_APPHOOKS \n
                4. create a new tuple {model_name_upper}_PLUGIN_TEMPLATES and add all templates from templates/ dir \n
                5. (optional): add ('{model_name_lower}', '{model_name}'), to PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES if the app should have categories\n
                6. ./manage.py makemigrations {app_label} ./manage.py migrate\n
            """
        ).format(
            app_label=app_label,
            app_path=app_path,
            model_name=model_name,
            model_name_upper=model_name.upper(),
            model_name_lower=model_name.lower(),
        )
        self.stdout.write(self.style.SUCCESS(msg))

