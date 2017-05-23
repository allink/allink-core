# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.utils.translation import activate
from django.core.urlresolvers import reverse

from cms.models import Page


def get_link_list(apps):
    links = {}
    link_apphooks = settings.PROJECT_LINK_APPHOOKS
    for apphook, url_names in link_apphooks.items():
        if apphook == 'Page':
            for lang_code, lang in settings.LANGUAGES:
                activate(lang_code)
                links.update({p.get_absolute_url(): {'page_id': p.id} for p in Page.objects.filter(publisher_is_draft=False)})

        else:
            for p in Page.objects.filter(application_urls=apphook, publisher_is_draft=False):
                for url_name, info in url_names.items():
                    obj_model = apps.get_model(info[0].split('.')[-3], info[0].split('.')[-1])
                    for lang_code, lang in settings.LANGUAGES:
                        activate(lang_code)
                        url_kwargs = {}
                        for obj in obj_model.objects.all():
                            for key in info[1]:
                                try:
                                    url_kwargs.update({key: getattr(obj, key)})
                                except AttributeError:
                                    try:
                                        url_kwargs.update({key: getattr(obj.translations.get(language_code=lang_code), key)})
                                    except:
                                        pass
                            full_url_name = u'{}:{}'.format(p.application_namespace, url_name)
                            try:
                                reversed_url = reverse(full_url_name, kwargs=url_kwargs)
                                links.update({reversed_url: {'link_apphook_page_id': p.id, 'link_url_name': full_url_name, 'link_object_id': obj.id, 'link_url_kwargs': info[1], 'link_model': info[0]}})
                            except:
                                continue
    return links


def migrate_links(apps, schema_editor):
    AllinkLegacyLink = apps.get_model("allink_legacy_redirect", "AllinkLegacyLink")
    Page = apps.get_model("cms", "Page")

    link_list = get_link_list(apps)
    print()

    for l in AllinkLegacyLink.objects.filter(new_page__isnull=False):
        if l.new_page in link_list:
            if 'page_id' in link_list[l.new_page]:
                l.link_page = Page.objects.get(id=link_list[l.new_page]['page_id'])
            else:
                l.link_apphook_page = Page.objects.get(id=link_list[l.new_page]['link_apphook_page_id'])
                l.link_object_id = link_list[l.new_page]['link_object_id']
                l.link_model = link_list[l.new_page]['link_model']
                l.link_url_name = link_list[l.new_page]['link_url_name']
                l.link_url_kwargs = link_list[l.new_page]['link_url_kwargs']
            l.save()
        else:
            print("\033[91m Kann nicht migriert werden.   id: ", l.id, ",  old:  ", l.old, ",  new_page:  ", l.new_page, "\033[0m")


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0011_auto_20170516_0349'),
        ('blog', '__latest__'),
        ('locations', '__latest__'),
        ('members', '__latest__'),
        ('people', '__latest__'),
        ('testimonials', '__latest__'),
        ('work', '__latest__'),
    ]

    operations = [
        migrations.RunPython(migrate_links, migrations.RunPython.noop)
    ]
