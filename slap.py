#!/usr/bin/python2

# Copyright (c) 2017 crito <crito@fnordpipe.org>

"""Usage:   slappy CMD

Process actions to setup ldap server

Arguments:
    CMD     select action to trigger

Commands:
    init    initialize empty base dn

"""

import docopt
import getpass
import ldap
import ldap.modlist as modlist

class slappy:
    ldapConn = None
    host = None
    username = None
    password = None

    def init(self):
        dn = raw_input('base-dn: ')
        dc = raw_input('dc: ')
        o = raw_input('organization: ')

        attrs = {}
        attrs['objectclass'] = [
            'organization',
            'dcObject'
        ]
        attrs['dc'] = dc
        attrs['o'] = o

        ldif = modlist.addModlist(attrs)
        self.ldapConn.add_s(dn, ldif)

    def run(self):
        args = docopt.docopt(__doc__)

        self.host = raw_input('url: ')
        self.username = raw_input('username: ')
        self.password = getpass.getpass('password: ')

        try:
            self.ldapConn = ldap.initialize(self.host)
            self.ldapConn.simple_bind_s(self.username, self.password)
        except ldap.LDAPError as e:
            print(e)

        if args['CMD'] == 'init':
            self.init()

        self.ldapConn.unbind_s()

if __name__ == '__main__':
    slappy().run()
