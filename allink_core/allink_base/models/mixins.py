# -*- coding: utf-8 -*-

from allink_core.allink_base.models import AllinkBaseAppContentPlugin

class AllinkManualEntriesMixin(object):
    def copy_relations(self, oldinstance):
        self.categories = oldinstance.categories.all()
        self.manual_entries = oldinstance.manual_entries.all()

    def get_selected_entries(self):
        return self.manual_entries.select_related()
