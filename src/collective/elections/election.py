# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from collective.elections import _

from plone.directives import dexterity, form
from borg.localrole.interfaces import ILocalRoleProvider

from zope.interface import Interface

from zope.interface import implements
from zope.component import adapts

from five import grok


class IElection(form.Schema):
    """Election
    """
    form.model("models/election.xml")


class View(dexterity.DisplayForm):
    grok.context(IElection)
    grok.require('zope2.View')

    def allowed_to_vote(self):
        wf_tool = getToolByName(self.context, "portal_workflow")
        chain = wf_tool.getChainForPortalType(self.context.portal_type)
        status = wf_tool.getStatusOf(chain[0], self.context)

        state = status['review_state']

        return state == 'voting'

    def status_change_msg(self):
        wf_tool = getToolByName(self.context, "portal_workflow")
        chain = wf_tool.getChainForPortalType(self.context.portal_type)
        status = wf_tool.getStatusOf(chain[0], self.context)

        state = status['review_state']

        wf_tr_map = {
                     'internal_revision': 'can-submit-to-public',
                     'public_revision': 'can-select-nominees',
                     'nominee_revision': 'can-send-to-public',
                     'public': 'can-be-started',
                     'voting': 'should-be-ended',
                     'scrutiny': 'results-should-be-public',
                     'published': 'can-be-closed',
                     }

        if state in wf_tr_map:
            trans_guard = getMultiAdapter((self.context, self.request),
                                        name=wf_tr_map[state])
            can_call_trans = trans_guard()

            if not can_call_trans:
                if state == 'internal_revision':
                    return _(u"Cannot send to public. You are not the CEO or you need to upload the signed configuration PDF and signature")
                if state == 'public_revision':
                    return _(u"Cannot select nominees. The date has not been reached")
                if state == 'nominee_revision':
                    return _(u"Cannot send to public. You are not the CEO or you need to upload the signed nomination and electoral PDF and signature")
                if state == 'public':
                    return _(u"Cannot start voting. The date has not been reached")
                if state == 'voting':
                    return _(u"Cannot start counting votes. The date has not been reached")
                if state == 'scrutiny':
                    return _(u"Cannot publish results. The date has not been reached")
                if state == 'published':
                    return _(u"Cannot close the election. You are not the CEO")

        return _(u"")



class ElectionLocalRoles(object):
    """
    Provide local roles for Elections

    XXX: This was taken literally from
    http://collective-docs.readthedocs.org/en/latest/security/dynamic_roles.html

    see if we can optimize it
    """

    implements(ILocalRoleProvider)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def getGeneralUserRolesOnContext(self, context, principal_id):
        """
        Calculate General User roles based on the user object.

        Note: This function is *heavy* since it wakes lots of objects along the acquisition chain.
        """

        # Filter out bogus look-ups - Plone calls this function
        # for every possible role look up out there, but
        # we are interested only these two cases
        if IElection.providedBy(context):
            if context.electoral_roll and (principal_id in context.electoral_roll):
                return ["General Users"]

        # No match
        return []

    def getRoles(self, principal_id):
        """Returns the roles for the given principal in context.

        This function is additional besides other ILocalRoleProvider plug-ins.

        @param context: Any Plone object
        @param principal_id: User login id
        """
        return self.getGeneralUserRolesOnContext(self.context, principal_id)

    def getAllRoles(self):
        """Returns all the local roles assigned in this context:
        (principal_id, [role1, role2])"""
        return [ ("general_users", ["General Users"]) ]
