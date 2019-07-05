# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse

from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from allink_core.core.loading import get_model

from allink_core.apps.locations.pdf import PdfLocations


Locations = get_model('locations', 'Locations')
LocationsAppContentPlugin = get_model('locations', 'LocationsAppContentPlugin')


class LocationsPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = Locations
    plugin_model = LocationsAppContentPlugin


class LocationsDetail(AllinkBaseDetailView):
    model = Locations


def export_pdf(request, id):
    date = (datetime.date.today().strftime('%d_%m_%Y'))

    item = Locations.objects.get(id=id)

    pdf = PdfLocations(item, request)
    output = pdf.build()
    filename = '%s_%s.pdf' % (item.title.replace(' ', '_'), date)

    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
