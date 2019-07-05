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
    template_name = 'work/work_detail.html'


class WorkSearchAjaxView(AllinkBaseAjaxFormView):
    form_class = WorkSearchForm
    plugin_class = WorkSearchPlugin

    def get_template_names(self):
        template_name = 'work/plugins/{}/_items.html'.format(self.plugin.template)
        return [template_name]


def export_pdf(request, id):
    date = (datetime.date.today().strftime('%d_%m_%Y'))

    item = Work.objects.get(id=id)

    pdf = PdfWork(item, request)
    output = pdf.build()
    filename = '%s_%s.pdf' % (item.title.replace(' ', '_'), date)

    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
