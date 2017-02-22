# -*- coding: utf-8 -*-
from django.db import models
from parler.managers import TranslatableManager

class AllinkTermsManager(TranslatableManager):
    def get_published(self):
        from .models import AllinkTerms
        return super(AllinkTermsManager, self).get(status=AllinkTerms.STATUS_PUBLISHED)
