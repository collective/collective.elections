# -*- coding: utf-8 -*-

from five import grok

from collective.elections.content import IElection

from Products.CMFCore.utils import getToolByName

from datetime import datetime


class CanSubmitToPublic(grok.View):
    grok.context(IElection)
    grok.name("can-submit-to-public")
    grok.require("cmf.ModifyPortalContent")

    def __call__(self):
        pm = getToolByName(self.context, 'portal_membership')
        
        auth_member = pm.getAuthenticatedMember()
        ceo = self.context.chief_electoral_officer  
        
        proper_user = auth_member.getMemberId() == ceo
        
        if not proper_user:
            return False
            
        # TODO: Check if the PDF and signature fields are populated. If not, fail
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
        
        
        
        
        