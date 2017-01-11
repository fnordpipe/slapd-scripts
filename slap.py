#!/usr/bin/python2

# Copyright (c) 2017 crito <crito@fnordpipe.org>

"""Usage:   slappy CMD

Process actions to setup ldap server

Arguments:
    CMD     select action to trigger

Commands:
    init    initialize empty base dn with user, group and service organizational unit

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
        baseDn = raw_input('Base DN: ')
        dc = raw_input('DC: ')
        o = raw_input('Organization: ')

        # base dn
        attrsList = []
        attrsList.append({ 'attrs': {} })
        attrsList[0]['dn'] = baseDn
        attrsList[0]['attrs']['objectclass'] = [
            'organization',
            'dcObject'
        ]
        attrsList[0]['attrs']['dc'] = dc
        attrsList[0]['attrs']['o'] = o

        # user dn
        attrsList.append({ 'attrs': {} })
        attrsList[1]['dn'] = 'ou=user,%s' % (baseDn)
        attrsList[1]['attrs']['objectclass'] = [
            'top',
            'organizationalUnit'
        ]
        attrsList[1]['attrs']['ou'] = 'user'

        # group dn
        attrsList.append({ 'attrs': {} })
        attrsList[2]['dn'] = 'ou=group,%s' % (baseDn)
        attrsList[2]['attrs']['objectclass'] = [
            'top',
            'organizationalUnit'
        ]
        attrsList[2]['attrs']['ou'] = 'group'

        # service dn
        attrsList.append({ 'attrs': {} })
        attrsList[3]['dn'] = 'ou=service,%s' % (baseDn)
        attrsList[3]['attrs']['objectclass'] = [
            'top',
            'organizationalUnit'
        ]
        attrsList[3]['attrs']['ou'] = 'service'

        for attrs in attrsList:
            print('adding entry: %s' % (attrs['dn']))
            ldif = modlist.addModlist(attrs['attrs'])
            self.ldapConn.add_s(attrs['dn'], ldif)

    def run(self):
        args = docopt.docopt(__doc__)

        self.host = raw_input('URL: ')
        self.username = raw_input('Username: ')
        self.password = getpass.getpass('Password: ')

        try:
            self.ldapConn = ldap.initialize(self.host)
            self.ldapConn.simple_bind_s(self.username, self.password)
        except ldap.LDAPError as e:
            print(e)

        if args['CMD'] == 'init':
            self.init()

        self.ldapConn.unbind_s()

if __name__ == '__main__':
    try:
        slappy().run()
    except KeyboardInterrupt as e:
        print('\nInterrupted by User')
