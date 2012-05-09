# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implements

from five import grok

from plone.directives import dexterity, form

from borg.localrole.interfaces import ILocalRoleProvider

from Products.CMFCore.utils import getToolByName

from collective.elections import _


class IElection(form.Schema):
    """ An election.
    """
    form.model("models/election.xml")


class View(dexterity.DisplayForm):
    grok.context(IElection)
    grok.require('zope2.View')

    def get_election_state(self):
        wf_tool = getToolByName(self.context, 'portal_workflow')
        chain = wf_tool.getChainForPortalType(self.context.portal_type)
        status = wf_tool.getStatusOf(chain[0], self.context)

        state = status['review_state']

        return state

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

    def is_public_revision(self):
        return self.get_election_state() == 'public_revision'

    def is_nominee_selection(self):
        return self.get_election_state() == 'nominee_selection'

    def is_public(self):
        return self.get_election_state() == 'public'

    def is_allowed_to_vote(self):
        if self.get_election_state() == 'voting':
            pm = getToolByName(self.context, 'portal_membership')

            auth_member = pm.getAuthenticatedMember()
            electoral_roll = self.context.electoral_roll

            return auth_member.getMemberId() in electoral_roll

        return False

    def is_counting(self):
        return self.get_election_state() == 'scrutiny'

    def is_published(self):
        return self.get_election_state() == 'published'

    def is_closed(self):
        return self.get_election_state() == 'closed'


class ElectionLocalRoles(object):
    """ Provide local roles for Elections

    XXX: This was taken literally from
    http://collective-docs.readthedocs.org/en/latest/security/dynamic_roles.html

    see if we can optimize it
    """

    implements(ILocalRoleProvider)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def getGeneralUserRolesOnContext(self, context, principal_id):
        """ Calculate General User roles based on the user object.

        Note: This function is *heavy* since it wakes lots of objects along
        the acquisition chain.
        """

        # Filter out bogus look-ups - Plone calls this function for every
        # possible role look up out there, but we are interested only these
        # two cases
        if IElection.providedBy(context):
            if context.electoral_roll and (principal_id in context.electoral_roll):
                return ["General Users"]

        # No match
        return []

    def getRoles(self, principal_id):
        """ Returns the roles for the given principal in context.

        This function is additional besides other ILocalRoleProvider plug-ins.

        @param context: Any Plone object
        @param principal_id: User login id
        """
        return self.getGeneralUserRolesOnContext(self.context, principal_id)

    def getAllRoles(self):
        """ Returns all the local roles assigned in this context:
        (principal_id, [role1, role2])
        """
        return []


# XXX: this views should be viewlets
class PublicRevision(dexterity.DisplayForm):
    """ This view is used in the Public Revision workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')


class NomineeSelection(dexterity.DisplayForm):
    """ This view is used in the Nominee Selection workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')


class Public(dexterity.DisplayForm):
    """ This view is used in the Public workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')


class Vote(dexterity.DisplayForm):
    """ This view is used in the Voting workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')


class Scrutiny(dexterity.DisplayForm):
    """ This view is used in the Scrutiny workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')


class Results(dexterity.DisplayForm):
    """ This view is used in the Published workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')


class Closed(dexterity.DisplayForm):
    """ This view is used in the Closed workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')
