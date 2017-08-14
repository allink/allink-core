# -*- coding: utf-8 -*-
import random
import requests
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from allink_core.core_apps.allink_instagram.models import AllinkInstagramPlugin


class AllinkInstagramPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkInstagramPlugin
        fields = (
            'template',
            'items_per_row',
            'paginated_by',
        )

    def __init__(self, *args, **kwargs):
        super(AllinkInstagramPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )


@plugin_pool.register_plugin
class CMSAllinkInstagramPlugin(CMSPluginBase):
    model = AllinkInstagramPlugin
    name = _('Instagram Feed')
    module = _('Generic')
    cache = False
    allow_children = False
    form = AllinkInstagramPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CMSAllinkInstagramPlugin, self).get_fieldsets(request, obj)
        fieldsets += (
            (None, {
                'fields': (
                    'ordering',
                    'follow_text',
                    'account',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder, file='content'):
        template = 'allink_instagram/plugins/{}/{}.html'.format(instance.template, file)
        return template

    def get_images(self, account_name='', max_id=''):
        image_urls = []
        # for reference: http://stackoverflow.com/questions/17373886/how-can-i-get-a-users-media-from-instagram-without-authenticating-as-a-user/33783840#33783840
        r = requests.get('https://www.instagram.com/{}/media/?max_id={}'.format(account_name, max_id))
        content = r.json()
        if hasattr(content, 'items'):
            for image in content['items']:
                image_urls.append({
                    'id': image['id'],
                    'link': image['link'],
                    'small': image['images']['low_resolution']['url'],
                    'big': image['images']['standard_resolution']['url'],
                    'caption': image['caption']['text']
                })
        return image_urls

    def get_follow_position(self, paginated_by):
        # if paginated_by is even
        if paginated_by % 2 == 0:
            return (paginated_by / 2) + 1
        else:
            # forlooper.counter starts at 1
            return 1

    def render(self, context, instance, placeholder):
        context = super(CMSAllinkInstagramPlugin, self).render(context, instance, placeholder)
        context['account_name'] = instance.account

        context['items_per_row'] = instance.items_per_row
        context['follow_text'] = instance.follow_text
        context['follow_position'] = self.get_follow_position(instance.paginated_by)

        cache_name = 'instagram_feed_{}'.format(instance.account)
        image_urls_cached = cache.get(cache_name, None)
        image_urls = []

        if not image_urls_cached:
            try:
                image_urls = self.get_images(account_name=instance.account)
                cache.set(cache_name, image_urls, 60 * 60)  # cache images for one hour
            except:
                return context
        else:
            image_urls = image_urls_cached

        if len(image_urls) > 0:
            if instance.ordering == 'random':
                image_urls_sample = random.sample(image_urls, instance.paginated_by)
                context['object_list'] = image_urls_sample
            else:
                context['object_list'] = image_urls[:instance.paginated_by]
        else:
            context['object_list'] = []
        return context
