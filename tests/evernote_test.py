# coding: utf-8

import unittest
from ConfigParser import SafeConfigParser

from everppt.evernote import Evernote

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
        self.evernote.authenticate('NOSUCHUSER', 'DUMMY')
        self.assertFalse(self.evernote.authenticated(), 'should not be authenticated')

    def test_list_notes(self):
        notes = self.evernote.list_notes()
