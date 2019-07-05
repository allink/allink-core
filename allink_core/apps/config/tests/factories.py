# -*- coding: utf-8 -*-
import factory
from allink_core.core.test.factories import FilerImageFactory
from ..models import Config, AllinkPageExtension, AllinkTitleExtension


class ConfigFactory(factory.DjangoModelFactory):

    class Meta:
        model = Config

    default_og_image = factory.SubFactory(FilerImageFactory)
    # theme_color
    # mask_icon_color
    # msapplication_tilecolor
    google_site_verification = 'google-site-verification-code'
    # default_to_email
    # default_from_email
    default_base_title = 'default base title'


class AllinkPageExtensionFactory(factory.DjangoModelFactory):

    class Meta:
        model = AllinkPageExtension

    extended_object = None
    og_image = factory.SubFactory(FilerImageFactory)
    teaser_image = factory.SubFactory(FilerImageFactory)


class AllinkTitleExtensionFactory(factory.DjangoModelFactory):

    class Meta:
        model = AllinkTitleExtension

    extended_object = None
    og_title = 'og title'
    og_description = 'og description'
    teaser_title = 'teaser title'
    teaser_technical_title = 'teaser technical title'
    teaser_description = 'teaser description'
    teaser_link_text = 'teaser link text'

