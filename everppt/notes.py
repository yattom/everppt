# coding: utf-8

from ConfigParser import SafeConfigParser

import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors


config = SafeConfigParser()
config.read("everppt.ini")

class Evernote(object):
    def __init__(self):
        self.auth_result = None

    def authenticate(self, username, password):
        evernoteHost = "sandbox.evernote.com"
        userStoreUri = "https://" + evernoteHost + "/edam/user"
        noteStoreUriBase = "https://" + evernoteHost + "/edam/note/"

        userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
        userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)

        userStore = UserStore.Client(userStoreProtocol)

        versionOK = userStore.checkVersion("Python EDAMTest",
                                           UserStoreConstants.EDAM_VERSION_MAJOR,
                                           UserStoreConstants.EDAM_VERSION_MINOR)
        api_key = config.get('evernote api', 'consumer_key')
        api_secret = config.get('evernote api', 'consumer_secret')

        self.auth_result = None
        try :
            self.auth_result = userStore.authenticate(username, password,
                                                api_key, api_secret)
        except Errors.EDAMUserException as e:
            # See http://www.evernote.com/about/developer/api/ref/UserStore.html#Fn_UserStore_authenticate
            parameter = e.parameter
            errorCode = e.errorCode
            errorText = Errors.EDAMErrorCode._VALUES_TO_NAMES[errorCode]
            raise StandardError(errorText)

    def authenticated(self):
        return self.auth_result != None

    def list_notes(self):
        pass
