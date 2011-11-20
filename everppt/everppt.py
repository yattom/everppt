# coding: utf-8

import sys

from notes import Evernote

def main():
    e = Evernote()
    e.authenticate(sys.argv[1], sys.argv[2])
    for n in e.list_notes():
        print "guid: %s"%(n.guid)
        print "title: %s"%(n.title.decode('utf-8'))
        print "content: %s"%(n.content)

if __name__=='__main__':
    main()

