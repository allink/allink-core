# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse

from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView, AllinkBaseAjaxFormView
from allink_core.core.loading import get_model, get_class

from allink_core.apps.work.pdf import PdfWork


Work = get_model('work', 'Work')
WorkAppContentPlugin = get_model('work', 'WorkAppContentPlugin')
WorkSearchPlugin = get_model('work', 'WorkSearchPlugin')
WorkSearchForm = get_class('work.forms', 'WorkSearchForm')


class WorkPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = Work
    plugin_model = WorkAppContentPlugin


class WorkDetail(AllinkBaseDetailView):
    model = Work


class WorkSearchAjaxView(AllinkBaseAjaxFormView):
    form_class = WorkSearchForm
    plugin_class = WorkSearchPlugin
    template_name = 'work/plugins/search/_items.html'


def export_pdf(request, id):
    date = (datetime.date.today().strftime('%d_%m_%Y'))

    item = Work.objects.get(id=id)

    pdf = PdfWork(item, request)
    output = pdf.build()
    filename = '%s_%s.pdf' % (item.title.replace(' ', '_'), date)

    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
