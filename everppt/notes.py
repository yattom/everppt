# coding: utf-8

from ConfigParser import SafeConfigParser

import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
from evernote.edam.notestore.ttypes import NoteFilter
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors


config = SafeConfigParser()
config.read("everppt.ini")

class Evernote(object):
    HOST = "sandbox.evernote.com"

    def __init__(self):
        self.auth_result = None
        self.__note_store = None

    def authenticate(self, username, password):
        api_key = config.get('evernote api', 'consumer_key')
        api_secret = config.get('evernote api', 'consumer_secret')

        user_store = self.create_user_store()
        self.auth_result = None
        try :
            self.auth_result = user_store.authenticate(username, password,
                                                api_key, api_secret)
            self.user = self.auth_result.user
            self.auth_token = self.auth_result.authenticationToken
        except Errors.EDAMUserException as e:
            # See http://www.evernote.com/about/developer/api/ref/UserStore.html#Fn_UserStore_authenticate
            parameter = e.parameter
            errorCode = e.errorCode
            errorText = Errors.EDAMErrorCode._VALUES_TO_NAMES[errorCode]
            raise StandardError(errorText)

    def authenticated(self):
        return self.auth_result != None

    def create_user_store(self):
        uri = "https://" + Evernote.HOST + "/edam/user"

        http_client = THttpClient.THttpClient(uri)
        protocol = TBinaryProtocol.TBinaryProtocol(http_client)

        user_store = UserStore.Client(protocol)

        version_ok = user_store.checkVersion("Python EDAMTest",
                                           UserStoreConstants.EDAM_VERSION_MAJOR,
                                           UserStoreConstants.EDAM_VERSION_MINOR)
        if not version_ok:
            raise StandardError("EDAM version error")

        return user_store

    def list_notes(self):
        note_store = self.note_store()
        filter = NoteFilter()
        notes = note_store.findNotes(self.auth_token, filter, 0, 40).notes
        return [Note(n, self) for n in notes]

    def note_store(self):
        if self.__note_store:
            return self.__note_store

        user = self.auth_result.user
        auth_token = self.auth_result.authenticationToken
        
        uri = "https://" + Evernote.HOST + "/edam/note/" + user.shardId
        http_client = THttpClient.THttpClient(uri)
        protocol = TBinaryProtocol.TBinaryProtocol(http_client)
        self.__note_store = NoteStore.Client(protocol)
        return self.__note_store


class Note(object):
    def __init__(self, note, evernote):
        self.note = note
        self.evernote = evernote
        self.fill_common_fields()
        self.__content = None

    def fill_common_fields(self):
        self.guid = self.note.guid
        self.title = self.note.title
        
    def get_content(self):
        if not self.__content:
            self.__content = self.evernote.note_store().getNoteContent(self.evernote.auth_token, self.guid)
        return self.__content
    content = property(get_content)


