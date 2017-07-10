# -*- coding: utf-8 -*-

from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from allink_core.core.loading import get_model

News = get_model('news', 'News')
NewsAppContentPlugin = get_model('news', 'NewsAppContentPlugin')


class NewsPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = News
    plugin_model = NewsAppContentPlugin


class NewsDetail(AllinkBaseDetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if not self.object.is_published():
            raise Http404(_('{} is not published.'.format(self.model.get_verbose_name())))
        else:
            return self.render_to_response(context)
