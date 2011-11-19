# coding: utf-8

import unittest
from ConfigParser import SafeConfigParser

from everppt.notes import Evernote

config = SafeConfigParser()
config.read("test.ini")


class EvernoteTest(unittest.TestCase):
    def setUp(self):
        self.evernote = Evernote()
        self.evernote.authenticate(config.get('evernote api', 'username'), 
                                   config.get('evernote api', 'password'))  

    def test_authenticate(self):
        self.assertTrue(self.evernote.authenticated(), 'should be authenticated')

    def test_authenticate_fail(self):
        try:
            self.evernote.authenticate('NOSUCHUSER', 'DUMMY')
            self.fail('should raise exception')
        except StandardError:
            pass
        self.assertFalse(self.evernote.authenticated(), 'should not be authenticated')

    def test_list_notes(self):
        notes = self.evernote.list_notes()
        self.assertTrue(type(notes) == list, 'notes should be a list')
        # TODO create a note and then test list_notes()
