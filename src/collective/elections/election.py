# -*- coding: utf-8 -*-

from zope.annotation.interfaces import IAnnotations

from zope.component import adapts
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import implements
from zope.security import checkPermission

from zope.schema.interfaces import IVocabularyFactory

from five import grok

from plone.directives import dexterity, form

from borg.localrole.interfaces import ILocalRoleProvider

from Products.CMFCore.interfaces import IActionSucceededEvent

from Products.CMFCore.utils import getToolByName

from collective.elections import _

from random import random


class IElection(form.Schema):
    """ An election.
    """
    form.model("models/election.xml")


class View(dexterity.DisplayForm):
    grok.context(IElection)
    grok.require('zope2.View')

    def __call__(self):
        if "chosen_nominee" in self.request:
            # A vote has been casted, let's store it
            self.cast_vote()
        return dexterity.DisplayForm.__call__(self)

    def cast_vote(self):
        pm = getToolByName(self.context, 'portal_membership')

        nominee = self.request.get("chosen_nominee")
        voter = pm.getAuthenticatedMember().getId()

        # Now, let's get the random number that belongs for this voter and
        # nominee
        annotation = IAnnotations(self.context)

        # XXX: Do some error checking, for now let's assume everything
        #      works fine
        random_number = annotation['electoral'][voter][nominee]

        # Finally, store the number in the annotation
        # XXX: From the documentation, we need to first concatenate a new
        #      random number, and get a hash from it. Also, we need to
        #      double encrypt it, and store that. For now, let's store it
        #      as it is.
        not_used_votes = annotation.get('not_used_votes', [])
        votes = annotation.get('votes', [])
        if random_number not in not_used_votes and\
           random_number not in votes:
            votes.append(random_number)
            annotation['votes'] = votes
        else:
            # XXX: This number shouldn't be usable, something wrong happened
            #      need to figure out how to proceed in this case
            print "CHEATING!"
            return

        # And now, we store the other possible random_numbers from this voter
        # Se they cannot be used
        not_used_votes += [i for i in annotation['electoral'][voter].values()
                                      if i != random_number]
        annotation['not_used_votes'] = not_used_votes

        # Finally, we "mark" the voter as "already_voted"
        annotation['electoral'][voter]['already_voted'] = True

        #Done.
        return

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

    def is_in_voting_state(self):
        return self.get_election_state() == 'voting'

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

    def is_allowed_to_vote(self):
        return checkPermission('collective.elections.canCastVote',
                               self.context)

    def has_already_voted(self):
        pm = getToolByName(self.context, 'portal_membership')
        voter = pm.getAuthenticatedMember().getId()

        annotation = IAnnotations(self.context)

        return (annotation['electoral'][voter]).get('already_voted', False)

class Scrutiny(dexterity.DisplayForm):
    """ This view is used in the Scrutiny workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')

    def get_voting_count(self):
        # XXX: This will go away, once the correct way for counting
        #      votes is implemented
        aux_results = {}
        results = []
        annotation = IAnnotations(self.context)
        nominees = annotation['nominees']
        votes = annotation['votes']
        for vote in votes:
            nominee = nominees[vote]
            nominee_count = aux_results.get(nominee, 0)
            nominee_count += 1
            aux_results[nominee] = nominee_count

        vocab = getUtility(IVocabularyFactory,
                           name="plone.principalsource.Users")
        values = vocab(self.context)

        for nominee in self.context.nominations_roll:
            full_name = values.getTermByToken(nominee).title
            results.append("%s: %s votes." % (full_name,
                                              aux_results.get(nominee,0)))

        return results

class Results(dexterity.DisplayForm):
    """ This view is used in the Published workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')

    def get_voting_count(self):
        # XXX: This will go away, once the correct way for counting
        #      votes is implemented
        aux_results = {}
        results = []
        annotation = IAnnotations(self.context)
        nominees = annotation['nominees']
        votes = annotation['votes']
        for vote in votes:
            nominee = nominees[vote]
            nominee_count = aux_results.get(nominee, 0)
            nominee_count += 1
            aux_results[nominee] = nominee_count

        vocab = getUtility(IVocabularyFactory,
                           name="plone.principalsource.Users")
        values = vocab(self.context)

        for nominee in self.context.nominations_roll:
            full_name = values.getTermByToken(nominee).title
            results.append("%s: %s votes." % (full_name,
                                              aux_results.get(nominee,0)))

        return results


class Closed(dexterity.DisplayForm):
    """ This view is used in the Closed workflow state.
    """
    grok.context(IElection)
    grok.require('zope2.View')

    def get_voting_count(self):
        # XXX: This will go away, once the correct way for counting
        #      votes is implemented
        aux_results = {}
        results = []
        annotation = IAnnotations(self.context)
        nominees = annotation['nominees']
        votes = annotation['votes']
        for vote in votes:
            nominee = nominees[vote]
            nominee_count = aux_results.get(nominee, 0)
            nominee_count += 1
            aux_results[nominee] = nominee_count

        vocab = getUtility(IVocabularyFactory,
                           name="plone.principalsource.Users")
        values = vocab(self.context)

        for nominee in self.context.nominations_roll:
            full_name = values.getTermByToken(nominee).title
            results.append("%s: %s votes." % (full_name,
                                              aux_results.get(nominee,0)))

        return results


class CastVote(dexterity.DisplayForm):
    """ This view is used to cast the vote.
    """
    grok.context(IElection)
    grok.require('collective.elections.canCastVote')

    def get_nominees(self):
        results = []
        # XXX: Find a way to get the vocabulary name from the field instead
        #      of having it hard-coded here
        vocab = getUtility(IVocabularyFactory,
                           name="plone.principalsource.Users")
        values = vocab(self.context)
        for id in self.context.nominations_roll:
            full_name = values.getTermByToken(id).title
            results.append((id,full_name))

        return results

@grok.subscribe(IElection, IActionSucceededEvent)
def generate_random_numbers_for_candidates(obj, event):
    """
    Here we will generate the random numbers for each candidate and each
    voter
    """

    #XXX: "digit_count" should be some customizable field from the election
    #     and not defined here.
    digit_count = 10

    if event.action != 'start':
        # If this is not the transition where the voting starts, then just
        # return
        return

    # Ok, let's generate our random numbers
    random_numbers = []
    total_numbers = len(obj.electoral_roll) * len(obj.nominations_roll)

    while len(random_numbers) < total_numbers:
        random_number = long(random()*(10**digit_count))
        if random_number not in random_numbers:
            random_numbers.append(random_number)

    # We have in random_numbers a whole list of unique random numbers
    # For now, we will store this in an annotation, perhaps we need to revise
    # this and store it somewhere else.
    annotation = IAnnotations(obj)
    nominee_annotation = {}
    electoral_annotation = {}

    # The idea here is to have 2 lists with len()=total_numbers which will
    # allow the use of zip built-in to assign each random number to
    # a nominee and a voter

    aux_nominees = obj.nominations_roll * len(obj.electoral_roll)
    aux_electoral = obj.electoral_roll * len(obj.nominations_roll)
    aux_electoral.sort()

    combination = zip(random_numbers, aux_electoral, aux_nominees)

    # Now, for each combination, we'll store it in the annotation
    for elem in combination:
        # First, let's store a dict with the number as key and the nominee
        # as value
        nominee_annotation[elem[0]] = elem[2]

        # Now, for the voter, we'll store a dict with the nominee and his
        # number
        vote_map = electoral_annotation.get(elem[1], {})
        vote_map[elem[2]] = elem[0]
        electoral_annotation[elem[1]] = vote_map
        # Also, let's mark it as "not already voted"
        electoral_annotation[elem[1]]['already_voted'] = False

    # Finally, store everything in the annotation and finish
    annotation['nominees'] = nominee_annotation
    annotation['electoral'] = electoral_annotation


@grok.subscribe(IElection, IActionSucceededEvent)
def count_votes(obj, event):

    if event.action != 'count':
        # If this is not the transition where the counting starts, then return
        return

    # At the moment we don't need this, we leave it as a placeholder for when
    # we need to decrypt to count, etc...
