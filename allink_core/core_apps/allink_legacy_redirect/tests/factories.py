# -*- coding: utf-8 -*-
import factory
from factory import fuzzy
from allink_core.core.test.factories import FilerImageFactory
from ..models import AllinkLegacyLink


class AllinkLegacyLinkFactory(factory.DjangoModelFactory):

    class Meta:
        model = AllinkLegacyLink

    old = '/old-path/'
    overwrite = '/new-path/'
    active = True
    match_subpages = False
    language = 'de'
    # last_test_result =
    # last_test_date =
    # skip_redirect_when_logged_in = False