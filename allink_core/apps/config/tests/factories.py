# -*- coding: utf-8 -*-
import factory
from django.conf import settings
from allink_core.core.test.factories import FilerImageFactory
from ..models import Config, AllinkPageExtension, AllinkTitleExtension


class ConfigFactory(factory.DjangoModelFactory):
    class Meta:
        model = Config

    default_og_image = factory.SubFactory(FilerImageFactory)
    theme_color = None
    mask_icon_color = None
    msapplication_tilecolor = None
    google_site_verification = 'google-site-verification-code'
    default_to_email = 'default_to_email@email.com'
    default_from_email = 'default_from_email@email.com'

    @factory.post_generation
    def post(self, create, extracted, **kwargs):
        for lang, _ in settings.LANGUAGES:
            self.set_current_language(lang)
            self.default_base_title = 'default_base_title_{}'.format(lang)
            self.newsletter_lead = 'newsletter_lead_{}'.format(lang)
            self.newsletter_signup_link = 'newsletter_signup_link_{}'.format(lang)
            self.newsletter_declaration_of_consent = 'newsletter_declaration_of_consent_{}'.format(lang)
            self.save()


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
