# -*- coding: utf-8 -*-

from datetime import datetime
from StringIO import StringIO

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from xhtml2pdf import pisa


class GenerateConfigurationPDF(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        html = ViewPageTemplateFile('templates/configuration_pdf.pt')(self)
        pdf = self.create_pdf(html)

        self.request.response.setHeader('Content-Type', 'application/pdf;;charset="utf-8"')
        return pdf.getvalue()

    def create_pdf(self, pdf_data):
        pdf = StringIO()
        pisa.pisaDocument(StringIO(pdf_data.encode('utf-8')), pdf, encoding='utf-8')

        return pdf

    def now(self):
        now = datetime.now()
        return now.isoformat()


class GenerateRollsPDF(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        html = ViewPageTemplateFile('templates/rolls_pdf.pt')(self)
        pdf = self.create_pdf(html)

        self.request.response.setHeader('Content-Type', 'application/pdf;;charset="utf-8"')
        return pdf.getvalue()

    def create_pdf(self, pdf_data):
        pdf = StringIO()
        pisa.pisaDocument(StringIO(pdf_data.encode('utf-8')), pdf, encoding='utf-8')

        return pdf

    def get_electoral_roll(self):
        """ Returns a list with the full name of all users in the electoral
        roll sorted alphabetically.
        """
        membership = getToolByName(self.context, 'portal_membership')

        roll = []
        for id in self.context.electoral_roll:
            #info = membership.getMemberInfo(id)
            #fullname = info['fullname'].decode('utf-8')
            roll.append(id)
        roll.sort()

        return roll

    def get_nominations_roll(self):
        return self.context.nominations_roll

    def now(self):
        now = datetime.now()
        return now.isoformat()
