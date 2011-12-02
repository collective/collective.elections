# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.CMFCore.WorkflowCore import WorkflowException

from matem.elections.testing import INTEGRATION_TESTING

ctype = 'matem.elections.election'
workflow_id = 'election_workflow'


class WorkflowTest(unittest.TestCase):

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
        self.failUnless(workflow_id in ids)

    def test_default_workflow(self):
        chain = self.workflow_tool.getChainForPortalType(self.obj.portal_type)
        self.failUnless(len(chain) == 1)
        self.failUnless(chain[0] == workflow_id)

    def test_workflow_initial_state(self):
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'configuration')

    def test_workflow_transitions(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'start')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'roll')
        self.workflow_tool.doActionFor(self.obj, 'sign')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'acceptance')
        self.workflow_tool.doActionFor(self.obj, 'confirm')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'confirmation')
        self.workflow_tool.doActionFor(self.obj, 'wait')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'waiting')
        self.workflow_tool.doActionFor(self.obj, 'code')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'coding')
        self.workflow_tool.doActionFor(self.obj, 'vote')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'voting')
        self.workflow_tool.doActionFor(self.obj, 'count')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'counting')
        self.workflow_tool.doActionFor(self.obj, 'validate')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'validating')
        self.workflow_tool.doActionFor(self.obj, 'publish')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'published')
        self.workflow_tool.doActionFor(self.obj, 'close')
        review_state = self.workflow_tool.getInfoFor(self.obj, 'review_state')
        self.assertEqual(review_state, 'closed')

    def test_workflow_permissions(self):
        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'start')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'start')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'sign')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'sign')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'confirm')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'confirm')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'wait')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'wait')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'code')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'code')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'start')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'vote')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'validate')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'validate')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'publish')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'publish')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        # guard-permission: Review portal content
        self.assertRaises(WorkflowException,
                          self.workflow_tool.doActionFor,
                          self.obj, 'close')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflow_tool.doActionFor(self.obj, 'close')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
