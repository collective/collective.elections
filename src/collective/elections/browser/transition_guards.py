# -*- coding: utf-8 -*-

from five import grok

from collective.elections.content import IElection

from Products.CMFCore.utils import getToolByName

from datetime import datetime


class CanSubmitToPublic(grok.View):
    grok.context(IElection)
    grok.name("can-submit-to-public")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):
        pm = getToolByName(self.context, 'portal_membership')
        
        auth_member = pm.getAuthenticatedMember()
        ceo = self.context.chief_electoral_officer  
        
        proper_user = auth_member.getMemberId() == ceo
        
        if not proper_user:
            return False
            
        if not (getattr(self.context, 'configuration_pdf') and\
                getattr(self.context, 'configuration_pdf_signature')):
            return False
            
        return True
        
    def render(self):
        return "can-submit-to-public"
        

class CanSelectNominees(grok.View):
    grok.context(IElection)
    grok.name("can-select-nominees")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):
        nsd = self.context.nominee_selection_date
        now = datetime.now()
        
        return now > nsd
        
    def render(self):
        return "can-select-nominees"


class CanSendToPublic(grok.View):
    grok.context(IElection)
    grok.name("can-send-to-public")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):
        pm = getToolByName(self.context, 'portal_membership')
        
        auth_member = pm.getAuthenticatedMember()
        ceo = self.context.chief_electoral_officer  
        
        proper_user = auth_member.getMemberId() == ceo
        
        if not proper_user:
            return False

        if not (getattr(self.context, 'rolls_pdf') and\
                getattr(self.context, 'rolls_pdf_signature')):
            return False
            
        return True
        
    def render(self):
        return "can-send-to-public"
                

class CanBeStarted(grok.View):
    grok.context(IElection)
    grok.name("can-be-started")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):
        vsd = self.context.voting_start_date
        now = datetime.now()
        
        return now > vsd
        
    def render(self):
        return "can-be-started"


class ShouldBeEnded(grok.View):
    grok.context(IElection)
    grok.name("should-be-ended")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):
        ved = self.context.voting_end_date
        now = datetime.now()
        
        return now > ved
        
    def render(self):
        return "should-be-ended"


class ResultsShouldGoPublic(grok.View):
    grok.context(IElection)
    grok.name("results-should-be-public")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):
        pd = self.context.publication_date
        now = datetime.now()
        
        return now > pd
        
    def render(self):
        return "results-should-be-public"


class CanBeClosed(grok.View):
    grok.context(IElection)
    grok.name("can-be-closed")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):
        pm = getToolByName(self.context, 'portal_membership')
        
        auth_member = pm.getAuthenticatedMember()
        ceo = self.context.chief_electoral_officer  
        
        proper_user = auth_member.getMemberId() == ceo
        
        if not proper_user:
            return False
            
        return True
        
    def render(self):
        return "can-be-closed"
                

