# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class PartnerQuerySet(AllinkCategoryModelQuerySet):
    pass


PartnerManager = PartnerQuerySet.as_manager
