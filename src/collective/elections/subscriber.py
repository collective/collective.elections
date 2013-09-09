# -*- coding: utf-8 -*-

from random import random

from zope.component import getMultiAdapter

from zope.annotation.interfaces import IAnnotations

from five import grok

from Products.CMFCore.interfaces import IActionSucceededEvent

from collective.elections.election import IElection

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.utils import getToolByName

@grok.subscribe(IElection, IActionSucceededEvent)
def generate_Users(obj, event):


    if event.action != 'send_to_public':
        # If this is not the transition where the users are confirmed, then just
        # return
        return

    
    optionele = obj.electoral_roll[3]
    optionnom = obj.nominations_roll[3]
    
    if u'default' in optionele.split('-'):
        obj.electors = obj.electoral_roll[0]

    if u'collection' in optionele.split('-'):
        
        catalog = getToolByName(obj, 'portal_catalog')
        res  = catalog.searchResults({'portal_type': 'Collection'})
        for elem in res:
            if elem.getObject().title == obj.electoral_roll[1][0]:
                collection = elem.getObject()
        
        lista = []
        for index in range(collection.results().length):
            person  = collection.results()[index]
            person = person.getObject()
            lista.append(person.id)

        obj.electors = lista
        
    if u'plaintext' in optionele.split('-'):     
        electors = obj.electoral_roll[2] 
        obj.electors = electors.split(', ')  

    if u'default' in optionnom.split('-'):
        obj.nomines = obj.nominations_roll[0]

    if u'collection' in optionnom.split('-'):
        catalog = getToolByName(obj, 'portal_catalog')
        res  = catalog.searchResults({'portal_type': 'Collection'})
        for elem in res:
            if elem.getObject().title == obj.nominations_roll[1][0]:
                collection = elem.getObject()
        lista = []
        for index in range(collection.results().length):
            person  = collection.results()[index]
            person = person.getObject()
            lista.append(person.id)

        obj.nomines = lista

    if u'plaintext' in optionnom.split('-'):     
        nomines = obj.nominations_roll[2] 
        obj.nomines = nomines.split(', ')  


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
    total_numbers = len(obj.electors) * len(obj.nomines)

    while len(random_numbers) < total_numbers:
        random_number = long(random() * (10 ** digit_count))

        # Make sure that the random number has digit_count digits:
        while len(str(random_number)) != digit_count:
            random_number = long(random() * (10 ** digit_count))

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

    
    aux_nominees = obj.nomines * len(obj.electors)
    aux_electoral = obj.electors * len(obj.nomines)
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
def save_votes(obj, event):

    if event.action != 'publish':
        return

    # After the voting has ended and the scrutiny is over, save the results
    # In an annotation so we can cleanup later
    context = obj
    request = obj.REQUEST
    annotation = IAnnotations(context)
    scrutiny = getMultiAdapter((context, request), name="scrutiny")

    annotation['final_results'] = scrutiny.get_voting_count()


@grok.subscribe(IElection, IActionSucceededEvent)
def cleanup_annotations(obj, event):

    if event.action != 'close':
        return

    # Remove all annotations except for the final results and receipts when closing
    context = obj
    annotation = IAnnotations(context)
    del annotation['votes']
    del annotation['nominees']
    del annotation['electoral']
    del annotation['not_used_votes']
