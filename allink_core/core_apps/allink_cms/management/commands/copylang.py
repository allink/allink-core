# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand

from cms.api import copy_plugins_to_language
from cms.models import Page, StaticPlaceholder, EmptyTitle
from cms.utils import get_language_list
from cms.utils.copy_plugins import copy_plugins_to


class Command(BaseCommand):
    """
    e.g.:
    ./manage.py copylang --from-lang=en --to-lang=nl --tree="Home"
    ./manage.py copylang --from-lang=en --to-lang=nl --tree_id=36
    ./manage.py copylang --from-lang=en --to-lang=nl --tree_id=36 --force
    """
    help = ('Duplicate the cms content from one lang to another '
            '(to boot a new language) using draft pages. '
            'If a page is given with the --tree_id option or --tree option '
            'only this page and its children are copied.')

    def add_arguments(self, parser):
        parser.add_argument('--from-lang', action='store', dest='from_lang', required=True,
                            help='Language to copy the content from.')
        parser.add_argument('--to-lang', action='store', dest='to_lang', required=True,
                            help='Language to copy the content to.')
        parser.add_argument('--site', action='store', dest='site',
                            help='Site to work on.')
        parser.add_argument('--force', action='store_false', dest='only_empty', default=True,
                            help='If set content is copied even if destination language already '
                                 'has content.')
        parser.add_argument('--skip-content', action='store_false', dest='copy_content',
                            default=True, help='If set content is not copied, and the command '
                                               'will only create titles in the given language.')
        parser.add_argument('--tree_id', action='store', dest='page_id',
                            type=int, default=None,
                            help='Only copy the page tree starting with '
                                 'page with the given id.')
        parser.add_argument('--tree', action='store', dest='page',
                            type=str, default=None,
                            help='Only copy the page tree starting with '
                                 'the given title in "from" language.')

    def handle(self, *args, **options):
        verbose = options.get('verbosity') > 1
        only_empty = options.get('only_empty')
        copy_content = options.get('copy_content')
        from_lang = options.get('from_lang')
        to_lang = options.get('to_lang')
        try:
            site = int(options.get('site', None))
        except Exception:
            site = settings.SITE_ID

        try:
            assert from_lang in get_language_list(site)
            assert to_lang in get_language_list(site)
        except AssertionError:
            raise CommandError('Both languages have to be present in settings.LANGUAGES and settings.CMS_LANGUAGES')

        if options.get('page_id', None):
            head = Page.objects.on_site(site) \
                .drafts().get(id=options.get('page_id'))
            pages = [head] + list(head.children.drafts())
        else:
            pages = Page.objects.on_site(site).drafts()
            if options.get('page', None):
                head = None
                for page in pages:
                    if page.get_title_obj(from_lang).title == options.get('page'):
                        if head is not None:
                            raise CommandError('Page has to be unique on the site. Try the --tree_id option.')
                        head = page
                pages = [head] + list(head.children.drafts())

        for page in pages:
            # copy title
            if from_lang in page.get_languages():
                title = page.get_title_obj(to_lang, fallback=False)
                if isinstance(title, EmptyTitle):
                    title = page.get_title_obj(from_lang)
                    if verbose:
                        self.stdout.write('copying title %s from language %s\n' % (title.title, from_lang))
                    title.id = None
                    title.publisher_public_id = None
                    title.publisher_state = 0
                    title.language = to_lang
                    title.save()
                if verbose:
                    self.stdout.write('copying plugins for %s from %s\n' % (page.get_page_title(from_lang), from_lang))
                if copy_content:
                    # copy plugins using API
                    copy_plugins_to_language(page, from_lang, to_lang, only_empty)
            else:
                if verbose:
                    self.stdout.write('Skipping page %s, language %s not defined\n' % (
                        page.get_page_title(page.get_languages()[0]), from_lang))

        if copy_content:
            for static_placeholder in StaticPlaceholder.objects.all():
                plugin_list = []
                for plugin in static_placeholder.draft.get_plugins():
                    if plugin.language == from_lang:
                        plugin_list.append(plugin)

                if plugin_list:
                    if verbose:
                        self.stdout.write(
                            'copying plugins from static_placeholder "%s" in "%s" to "%s"\n' % (
                                static_placeholder.name, from_lang, to_lang)
                        )
                    copy_plugins_to(plugin_list, static_placeholder.draft, to_lang)

        self.stdout.write('all done')
