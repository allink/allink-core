# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from allink_core.allink_categories.models import AllinkCategory


class AllinkManualEntriesMixin(object):

    def get_category_navigation(self):
        category_navigation = []
        # if manual entries are selected the category navigation
        # is created from all distinct categories in selected entries
        if self.manual_entries.count() > 0:
            for entry in self.manual_entries.all():
                for category in entry.categories.all():
                    if category not in category_navigation:
                        category_navigation.append(category)
        else:
            # override auto category nav
            if self.category_navigation.count() > 0:
                for category in self.category_navigation.all():
                    if self.get_render_queryset_for_display(category).exists():
                        category_navigation.append(category)
            # auto category nav
            else:
                for category in self.categories.all():
                    if self.get_render_queryset_for_display(category).exists():
                        category_navigation.append(category)
        return category_navigation

    def copy_relations(self, oldinstance):
        self.categories = oldinstance.categories.all()
        self.category_navigation = oldinstance.category_navigation.all()
        self.manual_entries = oldinstance.manual_entries.all()

    def get_selected_entries(self):
        return self.manual_entries.active()

    def get_render_queryset_for_display(self, category=None, filter=None):
        """
         returns all data_model objects distinct to id which are in the selected categories
          - category: category instance
          - filter: list tuple with model fields and value
            -> adds additional query
    
        """
        if self.categories.count() > 0 or category:
            """
             category selection
            """
            if category:
                queryset = self.data_model.objects.filter_by_category(category)
            else:
                queryset = self.data_model.objects.filter_by_categories(self.categories)

            return self._apply_ordering_to_queryset_for_display(queryset)

        else:
            """
             manual entries
             ordering is always like manual entries order (drag n drop)
             resulting instances are always specific classes of data_model
            """
            queryset = self.manual_entries.active()

            return queryset
