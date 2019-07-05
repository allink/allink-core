# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    """
    e.g.:
    ./manage.py clearcache"
    """
    help = ('Clears the hole application cache.')

    def handle(self, *args, **options):
        cache.clear()
