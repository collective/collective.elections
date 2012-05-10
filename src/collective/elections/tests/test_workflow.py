# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.elections.testing import INTEGRATION_TESTING

ctype = 'collective.elections.election'
workflow_id = 'election_workflow'


class WorkflowTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow_tool = getattr(self.portal, 'portal_workflow')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory(ctype, 'obj')
        self.obj = self.folder['obj']

    def test_workflow_installed(self):
        ids = self.workflow_tool.getWorkflowIds()
        self.assertTrue(workflow_id in ids)

    def test_default_workflow(self):
        chain = self.workflow_tool.getChainForPortalType(self.obj.portal_type)
        self.assertTrue(len(chain) == 1)
        self.assertTrue(chain[0] == workflow_id)

    def test_workflow_initial_state(self):
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'private')

    def test_workflow_transitions(self):
        self.workflow_tool.doActionFor(self.obj, 'submit')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'pending')
        setRoles(self.portal, TEST_USER_ID, ['Editor'])
        self.workflow_tool.doActionFor(self.obj, 'show')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'draft')
        self.workflow_tool.doActionFor(self.obj, 'wait')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'waiting')
        self.workflow_tool.doActionFor(self.obj, 'start')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'voting')
        self.workflow_tool.doActionFor(self.obj, 'count')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'scrutiny')
        self.workflow_tool.doActionFor(self.obj, 'publish')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'published')
        self.workflow_tool.doActionFor(self.obj, 'close')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'closed')
