# -*- coding: utf-8 -*-
import factory
from factory import fuzzy
from allink_core.core.test.factories import FilerImageFactory
from ..models import News, NewsAppContentPlugin


class NewsFactory(factory.DjangoModelFactory):

    class Meta:
        model = News

    title = factory.Sequence(lambda n: 'news entry %d' % n)
    # slug = ''
    lead = fuzzy.FuzzyText(length=500)
    preview_image = factory.SubFactory(FilerImageFactory)
    # template =
    # header_placeholder =
    # content_placeholder =


class NewsWithMetaFactory(NewsFactory):

    og_image = factory.SubFactory(FilerImageFactory)
    og_title = 'og title'
    og_description = 'og description'
    teaser_image = factory.SubFactory(FilerImageFactory)
    teaser_title = 'teaser title'
    teaser_technical_title = 'teaser technical title'
    teaser_description = 'teaser description'
    teaser_link_text = 'teaser link text'
    teaser_link_url = None
