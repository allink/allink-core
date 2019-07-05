# -*- coding: utf-8 -*-
import requests
from io import BytesIO
from requests.exceptions import MissingSchema
from PIL import Image as PILImage

from django.utils.translation import activate

from reportlab.platypus import BaseDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (Paragraph, PageTemplate, Frame, NextPageTemplate, Image, FrameBreak, PageBreak)
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.colors import Color
from reportlab.platypus.flowables import KeepTogether, ListFlowable, ListItem, HRFlowable
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from bs4 import BeautifulSoup

from cms.utils.plugins import get_plugins
from allink_core.core.utils import get_height_from_ratio, get_ratio_w_h


def clean(value):
    return value.replace('&', '&amp;')


pt = 0.353


def has_class(tag, cls):
    try:
        return True if tag['class'][0] == cls else False
    except KeyError:
        return False


def read_file_open(image):
    """
    used for drawImage
    reads a file from boto with its url/ and opens it
    returns a ImageReader object which can be directly be drawn
    needed, beacause media files cant be loaded directly from file stystem
    (they are stored on s3)
    """
    try:
        return PILImage.open(BytesIO(requests.get(image.url).content))
    except MissingSchema:
        # localhost (read file from local file system)
        return image.path


def read_file(image):
    """
    used for Image(Flowable)
    reads a file from boto with its url
    returns a ImageReader object which can be directly be drawn
    needed, beacause media files cant be loaded directly from file stystem
    (they are stored on s3)
    """
    try:
        return BytesIO(requests.get(image.url).content)
    except MissingSchema:
        # localhost (read file from local file system)
        return image.path


def set_links(tag):
    import re

    from cms.models.pluginmodel import CMSPlugin
    from allink_core.core.utils import base_url

    cleaned = str(tag)
    links = tag.findAll('cms-plugin')
    for link in links:
        if link['alt'].startswith('Button'):
            button = CMSPlugin.objects.get(id=link['id']).get_plugin_instance()[0]
            btn_reg = re.compile('<cms-plugin alt="Button.*?id="%s".*?</cms-plugin>' % link['id'])
            cleaned = re.sub(btn_reg.pattern, r'<link href="%s"><u>%s</u></link>'
                             % (base_url() + button.link_url_typed,
                                button.label), str(cleaned),
                             flags=re.DOTALL)
    return cleaned


def extract_content_from_text_plugin(plugin):
    """
    returns a list with tuples
    ('title-h1', '<<content>>'),
    ...
    """
    body = plugin.get_plugin_instance()[0].body
    soup = BeautifulSoup(body)
    tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'ul'])
    content = ()
    for tag in tags:
        # title
        if tag.name == 'h1':
            tag = set_links(tag)
            content += ('title-h1', str(tag)),
        elif tag.name == 'h2':
            tag = set_links(tag)
            content += ('title-h2', str(tag)),
        elif tag.name == 'h3':
            tag = set_links(tag)
            content += ('title-h3', str(tag)),
        # text
        elif has_class(tag, 'lead'):
            tag = set_links(tag)
            content += ('text-lead', str(tag)),
        elif has_class(tag, 'medium'):
            tag = set_links(tag)
            content += ('text-medium', str(tag)),
        elif has_class(tag, 'small'):
            tag = set_links(tag)
            content += ('text-small', str(tag)),
        # lists
        elif tag.name == 'ul':
            content += ('list-bullet', map(lambda x: set_links(x), tag.findAll('li'))),
        else:
            # fallback and if no class is defined
            tag = set_links(tag)
            content += ('text-normal', str(tag)),
    return content


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1:
            self.setFont("MessinaSansRegular", 7.5, 9.5)
            self.drawRightString(147.25 * mm, 288 * mm, '{}/{}'.format(self._pageNumber, page_count))


class PdfLocations:

    page_templates = None

    floatings = []

    pagesize = A4
    rightMargin = 6.5 * mm
    leftMargin = 18 * mm
    topMargin = 7 * mm
    bottomMargin = 7 * mm

    def __init__(self, item, request, *args, **kwargs):

        pdfmetrics.registerFont(TTFont('AerotypeZoojaLight', 'static/fonts/pdf/Aerotype-Zooja-Light.ttf'))
        pdfmetrics.registerFont(TTFont('MessinaSansBold', 'static/fonts/pdf/MessinaSans-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('MessinaSansRegular', 'static/fonts/pdf/MessinaSans-Regular.ttf'))

        pdfmetrics.registerFontFamily('MessinaSans', normal='MessinaSansRegular', bold='MessinaSansBold',)
        pdfmetrics.registerFontFamily('AerotypeZoojaLight', normal='AerotypeZoojaLight',)

        self.output = BytesIO()
        self.item = item
        self.language = request.LANGUAGE_CODE
        self.logo = ImageReader('static/images/branding/hr-campus-logo-and-claim.png')

        self.doc = BaseDocTemplate(
            filename=self.output,
            pagesize=self.pagesize,
            rightMargin=self.rightMargin,
            leftMargin=self.leftMargin,
            topMargin=self.topMargin,
            bottomMargin=self.bottomMargin
        )
        self.first_page_settings = {
            'header_height': 5 * mm,
            'footer_height': 28 * mm,
            'preview_image_width': 52.75 * mm,
            'preview_image_height': 52.75 * mm,
        }
        self.later_page_settings = {
            'header_height': 15 * mm,
            'footer_height': 28 * mm,
        }
        self.frames = {}

        self.request = request
        self.transparent = Color(0, 0, 0, alpha=0.7)
        self.brand_color = HexColor(0xFAE600)
        self.font_color = HexColor(0x43494d)
        self.init_page_templates()
        self.styles = self.get_stylesheets()

        # contnet from placeholders
        self.allowed_header_plugins = [
            'TextPlugin',
        ]
        self.allowed_content_plugins = [
            'TextPlugin',
            'CMSAllinkImagePlugin',
            'CMSAllinkPageBreakPlugin',
        ]

        self.header_plugins = self.get_relevant_header_plugins()
        self.content_plugins = self.get_relevant_content_plugins()

    def init_page_templates(self):

        self.doc.addPageTemplates(
            [
                PageTemplate(
                    id='first_page',
                    pagesize=self.pagesize,
                    onPage=self.on_first_page,
                    frames=[
                        Frame(
                            152.25 * mm,
                            0,
                            width=self.first_page_settings['preview_image_width'],
                            height=233.75 * mm,
                            bottomPadding=(2 * self.bottomMargin) + self.first_page_settings['footer_height'],
                            leftPadding=0,
                            rightPadding=0,
                        ),
                        Frame(
                            self.leftMargin,
                            0,
                            width=129.25 * mm,
                            height=self.doc.height,
                            bottomPadding=self.first_page_settings['footer_height'],
                            topPadding=0,
                            leftPadding=0,
                            rightPadding=0,
                        )
                    ]
                ),
                PageTemplate(
                    id='later_page',
                    pagesize=A4,
                    onPage=self._later_pages,
                    frames=[
                        Frame(
                            self.leftMargin,
                            0,
                            width=129.25 * mm,
                            height=self.doc.height,
                            bottomPadding=self.later_page_settings['footer_height'],
                            topPadding=0,
                            leftPadding=0,
                            rightPadding=0,
                        )
                    ]
                )
            ]
        )

        self.floatings.append(NextPageTemplate('later_page'))

    def get_stylesheets(self):
        stylesheet = StyleSheet1()

        # PDF styles
        stylesheet.add(ParagraphStyle(name='pre-title',
                                      fontName='MessinaSansBold',
                                      fontSize=9,
                                      textColor=self.font_color,
                                      leading=9.5
                                      )
                       )
        stylesheet.add(ParagraphStyle(name='main-title',
                                      fontName='AerotypeZoojaLight',
                                      fontSize=48,
                                      textColor=self.font_color,
                                      leading=45,
                                      spaceAfter=7 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='sub-title',
                                      fontName='MessinaSansBold',
                                      fontSize=14,
                                      textColor=self.font_color,
                                      leading=22,
                                      spaceAfter=17.25 * mm)
                       )
        # ckeditor styles
        stylesheet.add(ParagraphStyle(name='title-h1',
                                      fontName='MessinaSansBold',
                                      fontSize=9,
                                      textColor=self.font_color,
                                      leading=9.5,
                                      spaceAfter=2.25 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='title-h2',
                                      fontName='AerotypeZoojaLight',
                                      fontSize=48,
                                      textColor=self.font_color,
                                      leading=45,
                                      spaceAfter=7 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='title-h3',
                                      fontName='MessinaSansBold',
                                      fontSize=14,
                                      textColor=self.font_color,
                                      leading=22,
                                      spaceAfter=0.2 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='text-lead',
                                      fontName='MessinaSansBold',
                                      fontSize=14,
                                      textColor=self.font_color,
                                      leading=22,
                                      spaceAfter=7 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='text-medium',
                                      fontName='MessinaSansRegular',
                                      fontSize=14,
                                      textColor=self.font_color,
                                      leading=18,
                                      spaceAfter=7 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='text-normal',
                                      fontName='MessinaSansRegular',
                                      fontSize=10,
                                      textColor=self.font_color,
                                      leading=14,
                                      spaceAfter=5.25 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='text-normal-link',
                                      fontName='MessinaSansRegular',
                                      fontSize=10,
                                      textColor=self.font_color,
                                      leading=14,
                                      spaceAfter=5.25 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='text-small',
                                      fontName='MessinaSansRegular',
                                      fontSize=8.5,
                                      textColor=self.font_color,
                                      leading=14,
                                      spaceAfter=3.25 * mm)
                       )
        stylesheet.add(ParagraphStyle(name='list-bullet',
                                      fontName='MessinaSansRegular',
                                      fontSize=10,
                                      textColor=self.font_color,
                                      leading=14,)
                       )
        stylesheet.add(ParagraphStyle(name='list-number',
                                      fontName='MessinaSansRegular',
                                      fontSize=10,
                                      textColor=self.font_color,
                                      leading=14,
                                      spaceAfter=5.25 * mm)
                       )
        return stylesheet

    def draw_main_image(self, canvas, doc):
        canvas.setFillColor(self.brand_color)
        canvas.rect(152.25 * mm, self.doc.height - 43.75 * mm, 52.75 * mm, 52.75 * mm, stroke=0, fill=1)
        if self.item.preview_image:
            canvas.drawImage(ImageReader(read_file_open(self.item.preview_image)), 152.25 * mm,
                             self.doc.height - 43.75 * mm, mask='auto', width=52.75 * mm, height=52.75 * mm)

    def draw_footer(self, canvas, doc):
        canvas.setFont('MessinaSansRegular', 7.5, 9.5)
        canvas.setFillColor(self.font_color)
        w, h = self.logo.getSize()
        ratio = h / float(w)
        # static files can be loaded directly from file stystem
        canvas.drawImage(self.logo, self.leftMargin, 7 * mm, mask='auto', width=49.7 * mm, height=(49.7 * mm * ratio))

        canvas.drawString(107.5 * mm, 22 * mm - self.bottomMargin, 'HR Campus AG')
        canvas.drawString(107.5 * mm, 18.5 * mm - self.bottomMargin, 'Kriesbachstrasse 3')
        canvas.drawString(107.5 * mm, 15 * mm - self.bottomMargin, 'CH-8600 Dübendorf')

        canvas.drawString(152.25 * mm, 22 * mm - self.bottomMargin, '+41 44 215 15 15')
        canvas.drawString(152.25 * mm, 18.5 * mm - self.bottomMargin, 'office@hr-campus.ch')
        canvas.drawString(152.25 * mm, 15 * mm - self.bottomMargin, 'www.hr-campus.ch')

    def draw_line(self, canvas, doc):
        canvas.line(doc.leftMargin, 22 * mm, 52.75 * mm + 129.25 * mm, 22 * mm)

    def on_first_page(self, canvas, doc):
        self.draw_main_image(canvas, doc)
        self.draw_line(canvas, doc)
        self.draw_footer(canvas, doc)

    def _later_pages(self, canvas, doc):
        canvas.setFont('MessinaSansBold', 7.5, 9.5)
        # break line when title to long
        title_area = simpleSplit(clean(self.item.title), canvas._fontname, canvas._fontsize,
                                 self.first_page_settings['preview_image_width'])
        x = 152.25 * mm
        y = 288 * mm
        for line in title_area:
            canvas.drawString(x, y, line)
            y -= canvas._leading

        # canvas.drawString(152.25 * mm, 288 * mm, clean(self.item.title))
        self.draw_line(canvas, doc)
        self.draw_footer(canvas, doc)

    def get_relevant_header_plugins(self):
        """
        returns a list with only relevant plugins which are allowed in header_placeholder
        Plugins are directly inside the placeholder
        """
        all_plugins = get_plugins(
            request=self.request,
            placeholder=self.item.header_placeholder,
            template=None,
        )
        relevant_plugins = []

        for plugin in all_plugins:
            if plugin.plugin_type in self.allowed_header_plugins:
                relevant_plugins.append(plugin)
            elif plugin.plugin_type == 'CMSAllinkContentPlugin' and not plugin.ignore_in_pdf:
                relevant_plugins.append(plugin)
        return relevant_plugins

    def get_relevant_content_plugins(self):
        """
        returns a list with only relevant plugins from a queryset of plugins
        Plugins are always children of CMSAllinkContentColumnPlugin or CMSAllinkContentPlugin itself
        """
        all_plugins = get_plugins(
            request=self.request,
            placeholder=self.item.content_placeholder,
            template=None,
            lang=self.language,
        )
        relevant_plugins = []
        for plugin in all_plugins:
            if plugin.plugin_type == 'CMSAllinkContentPlugin':
                # at the moment only templates 'col-1' and 'col-1-1' are supported
                if not plugin.ignore_in_pdf and (plugin.template == 'col-1' or plugin.template == 'col-1-1'):
                    relevant_plugins.append(plugin)
                    column_plugins = plugin.get_children()
                    for column in column_plugins:
                        for child in column.get_children():
                            # exlude images which are used as background icons
                            if not getattr(child.get_plugin_instance()[0], 'project_css_classes', False):
                                # also skip ImagePlugins which are inside a content plugin with template col-1-1
                                if plugin.template == 'col-1-1' and child.plugin_type == 'CMSAllinkImagePlugin':
                                    continue
                                if child.plugin_type in self.allowed_content_plugins:
                                    relevant_plugins.append(child.get_plugin_instance()[0])
            elif plugin.plugin_type == 'CMSAllinkPageBreakPlugin':
                relevant_plugins.append(plugin)
        return relevant_plugins

    def append_pagebreak_plugin(self, plugin):
        self.floatings.append(PageBreak())

    def append_text_plugin(self, plugin):
        content = extract_content_from_text_plugin(plugin)

        for tag in content:
            # all types of lists
            if tag[0] == 'list-bullet' or tag[0] == 'list-number':
                list_flowables = []
                for item in tag[1]:
                    list_flowables.append(ListItem(Paragraph(item, self.styles[tag[0]]),
                                                   leftIndent=10, value='circle'))
                self.floatings.append(ListFlowable(list_flowables,
                                                   bulletType='bullet',
                                                   start='circle',
                                                   leftIndent=10,
                                                   bulletFontSize=3,
                                                   bulletOffsetY=-4,
                                                   spaceAfter=4 * mm))
            # all types paragraph styles
            # title - h1, title - h2, title - h3,
            # text - lead, text - normal, text - small
            else:
                self.floatings.append(KeepTogether(Paragraph(tag[1], self.styles[tag[0]])))
                if tag[0] == 'title-h3':
                    self.floatings.append(HRFlowable(spaceBefore=0.2 * mm, spaceAfter=5.25 * mm,
                                                     color=self.transparent, thickness=0.5, width='100%'))

    def append_image_plugin(self, plugin):
        if hasattr(plugin.djangocms_image_allinkimageplugin, 'picture'):
            picture_plug = plugin.djangocms_image_allinkimageplugin
            if picture_plug.picture:
                image = picture_plug.picture
                width = 129.25 * mm  # is same as Frame.width
                # use ratio from plugin
                if picture_plug.ratio and picture_plug.ratio != 'x-y':
                    ratio_w, ratio_h = get_ratio_w_h(picture_plug.ratio)
                # use original ratio
                else:
                    ratio_w = image.width
                    ratio_h = image.height
                height = get_height_from_ratio(width, ratio_w, ratio_h)

                self.floatings.append(Image(read_file(image), width=width, height=height,
                                            mask='auto', hAlign='LEFT', ))
                self.floatings.append(Paragraph('', self.styles['main-title']))

    def append_content_plugin(self, plugin):
        # render the title of the section in the corresponding style
        # styles: title - h1, title - h2, title - h3

        if plugin.title:
            self.floatings.append(KeepTogether(Paragraph(clean(plugin.title),
                                                         self.styles['title-{}'.format(plugin.title_size)])))
            if plugin.title_size == 'h3':
                self.floatings.append(HRFlowable(spaceBefore=0.2 * mm, spaceAfter=5.25 * mm,
                                                 color=self.transparent, thickness=0.5, width='100%'))

    def append_plugins(self, plugins):
        for plugin in plugins:
            if plugin.plugin_type == 'CMSAllinkPageBreakPlugin':
                self.append_pagebreak_plugin(plugin)
            elif plugin.plugin_type == 'TextPlugin':
                self.append_text_plugin(plugin)
            elif plugin.plugin_type == 'CMSAllinkImagePlugin':
                self.append_image_plugin(plugin)
            elif plugin.plugin_type == 'CMSAllinkContentPlugin':
                self.append_content_plugin(plugin)

    def build(self):
        activate(self.language)

        self.floatings.append(HRFlowable(spaceBefore=0.2 * mm, spaceAfter=5.25 * mm, color=self.transparent,
                                         thickness=0.5, width='100%'))

        self.floatings.append(FrameBreak())

        # page title
        self.floatings.append(Paragraph(clean(self.request.current_page.get_title()), self.styles['pre-title']))

        # main title
        self.floatings.append(Paragraph(clean(self.item.title), self.styles['main-title']))

        # sub title
        self.floatings.append(Paragraph(clean(self.item.lead), self.styles['sub-title']))

        # content
        self.append_plugins(self.header_plugins)
        self.append_plugins(self.content_plugins)

        self.doc.build(self.floatings, canvasmaker=NumberedCanvas)
        return self.output
