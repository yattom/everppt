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
        api_key = config.get('evernote api', 'consumer_key')
        api_secret = config.get('evernote api', 'consumer_secret')

        user_store = self.create_user_store()
        self.auth_result = None
        try :
            self.auth_result = user_store.authenticate(username, password,
                                                api_key, api_secret)
        except Errors.EDAMUserException as e:
            # See http://www.evernote.com/about/developer/api/ref/UserStore.html#Fn_UserStore_authenticate
            parameter = e.parameter
            errorCode = e.errorCode
            errorText = Errors.EDAMErrorCode._VALUES_TO_NAMES[errorCode]
            raise StandardError(errorText)

    def authenticated(self):
        return self.auth_result != None

    def create_user_store(self):
        host = "sandbox.evernote.com"
        uri = "https://" + host + "/edam/user"

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
        pass
