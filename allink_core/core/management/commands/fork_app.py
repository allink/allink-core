# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils import six

from allink_core.core.customisation.utils import fork_allink_app


class Command(BaseCommand):
    help = ("Create a local version of an app in 'allink_core.apps'.")

    def add_arguments(self, parser):
        parser.add_argument(
            'dummy_app',
            help='The module to copy the files from',
            nargs='?',
            default='allink_core.core.customisation.dummy_fork_app_minimum'
        )
        parser.add_argument('app_label', help="The application name of the app in 'allink_core.apps'")
        parser.add_argument('app_path', help='The path to copy the files to')
        parser.add_argument(
            '-e',
            '--example',
            action='store_true',
            help='Creates all the files which can be overwritten including a sample implementation.',
        )

    def handle(self, *args, **options):

        dummy_app = options['dummy_app']
        app_label = options['app_label']
        app_path = options['app_path']
        example = options['example']

        if example:
            dummy_app = 'allink_core.core.customisation.dummy_fork_app_example'

        try:
            fork_allink_app(
                dummy_app=dummy_app,
                app_label=app_label,
                app_path=app_path
            )
        except Exception as e:
            raise CommandError(six.text_type(e))

        msg = (
            """
            The final steps:\n
            1. add '{app_path}.{app_label}', to OVERRIDDEN_ALLINK_CORE_APPS \n
            2. if you have already overwritten templates in the project templates dir, move them to {app_path}/{app_label}/templates/{app_label} \n
            """  # noqa
        ).format(
            app_label=app_label,
            app_path=app_path,
        )

        if example:
            msg += (
                """
                3. make sure you remove all files which you don't need! (be generouse here, you can always have peek into version control later.)\n
                4. make sure you remove all comments which you don't need! (be generouse here, you can always have peek into version control later.)\n
                """  # noqa
            )
        self.stdout.write(self.style.SUCCESS(msg))
