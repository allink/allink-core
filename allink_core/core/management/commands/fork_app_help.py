# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand, CommandError
from django.utils import six

from allink_core.core.customisation.fork_app import fork_app


class Command(BaseCommand):
    help = (
        "Create a local version of one of allink's app so it can "
        "be customised. Also includes helpeful comments to get you started.")

    def add_arguments(self, parser):
        parser.add_argument('app_label', help='The application to fork')
        parser.add_argument('target_path', help='The path to copy the files to')

    def handle(self, *args, **options):
        # Use a stdout logger
        logger = logging.getLogger(__name__)
        stream = logging.StreamHandler(self.stdout)
        logger.addHandler(stream)
        logger.setLevel(logging.DEBUG)

        app_label, folder_path = options['app_label'], options['target_path']
        try:
            fork_app(app_label, folder_path, logger, help=True)
        except Exception as e:
            raise CommandError(six.text_type(e))
