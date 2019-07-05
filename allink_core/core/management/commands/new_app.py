# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand, CommandError
from django.utils import six

from allink_core.core import customisation


class Command(BaseCommand):
    help = (
        "Create a new app with all the basic functionality a allink app has.")

    def add_arguments(self, parser):
        parser.add_argument('app_label', help='The application name')
        parser.add_argument('target_path', help='The path to copy the files to')

    def handle(self, *args, **options):
        # Use a stdout logger
        logger = logging.getLogger(__name__)
        stream = logging.StreamHandler(self.stdout)
        logger.addHandler(stream)
        logger.setLevel(logging.DEBUG)

        app_label, folder_path = options['app_label'], options['target_path']
        try:
            customisation.new_app(app_label, folder_path, logger)
        except Exception as e:
            raise CommandError(six.text_type(e))
