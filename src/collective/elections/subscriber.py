# -*- coding: utf-8 -*-

from random import random

from zope.annotation.interfaces import IAnnotations

from five import grok

from Products.CMFCore.interfaces import IActionSucceededEvent

from collective.elections.election import IElection


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
