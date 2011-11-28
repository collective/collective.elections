# -*- coding: utf-8 -*-

from five import grok
from plone.directives import form


class IElection(form.Schema):
    """Election
    """
    form.model("models/election.xml")
