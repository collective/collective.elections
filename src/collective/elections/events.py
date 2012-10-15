# -*- coding: utf-8 -*-

from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from collective.elections.election import IElection

from Products.CMFCore.utils import getToolByName


def remove_configuration_pdf(obj):
    """
    Remove the configuration PDF and signature that is supposed to be added
    under "Internal Revision" state
    """

    setattr(obj, 'configuration_pdf', None)
    setattr(obj, 'configuration_pdf_signature', None)


def remove_nominees_pdf(obj):
    """
    Remove the nominees PDF and signature that is supposed to be added
    under "Nominees" state
    """

    setattr(obj, 'rolls_pdf', None)
    setattr(obj, 'rolls_pdf_signature', None)


def count_votes(obj):
    """
    Count the total number of votes for the election
    """

    pass


@grok.subscribe(IElection, IActionSucceededEvent)
def state_changed(obj, event):
    """
    This function will be fired every time an election changes state.
    The idea is to take specific action depending on which is the new state
    """

    wf_tool = getToolByName(obj, "portal_workflow")
    chain = wf_tool.getChainForPortalType(obj.portal_type)
    status = wf_tool.getStatusOf(chain[0], obj)

    state = status['review_state']

    if state == 'private':
        remove_configuration_pdf(obj)
    elif state == 'nominee_selection':
        remove_nominees_pdf(obj)
    elif state == 'scrutiny':
        count_votes(obj)
