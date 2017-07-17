# -*- coding: utf-8 -*-
from parler.managers import TranslatableManager


class AllinkTermsManager(TranslatableManager):
    def get_published(self):
        from allink_core.core_apps.allink_terms.models import AllinkTerms
        return super(AllinkTermsManager, self).get(status=AllinkTerms.STATUS_PUBLISHED)
