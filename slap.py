#!/usr/bin/python2

# Copyright (c) 2017 crito <crito@fnordpipe.org>

"""Usage:   slap.py [-v]

initialize an empty ldap server

Options:
    -v  Verbose

Example:
   URL: ldap://ldap.example.org:389/
   Base DN: dc=example,dc=org
   Username: root
   Password:
   DC Name: example
   Organization: example organization
   # ldap: add entry: dc=example,dc=org
   # ldap: add entry: ou=user,dc=example,dc=org
   # ldap: add entry: ou=group,dc=example,dc=org
   # ldap: add entry: ou=service,dc=example,dc=org
   # ldap: add entry: cn=root,dc=example,dc=org

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
    baseDn = None
    dc = None
    o = None
    verbose = False

    def add(self, attrs):
        if self.verbose == True:
            print('# ldap: add entry: %s' % (attrs['dn']))

        ldif = modlist.addModlist(attrs['attrs'])
        self.ldapConn.add_s(attrs['dn'], ldif)

    def createBaseDn(self):
        # base dn
        attrsList = []
        attrsList.append({ 'attrs': {} })
        attrsList[0]['dn'] = self.baseDn
        attrsList[0]['attrs']['objectclass'] = [
            'organization',
            'dcObject'
        ]
        attrsList[0]['attrs']['dc'] = self.dc
        attrsList[0]['attrs']['o'] = self.o

        # user dn
        attrsList.append({ 'attrs': {} })
        attrsList[1]['dn'] = 'ou=user,%s' % (self.baseDn)
        attrsList[1]['attrs']['objectclass'] = [
            'top',
            'organizationalUnit'
        ]
        attrsList[1]['attrs']['ou'] = 'user'

        # group dn
        attrsList.append({ 'attrs': {} })
        attrsList[2]['dn'] = 'ou=group,%s' % (self.baseDn)
        attrsList[2]['attrs']['objectclass'] = [
            'top',
            'organizationalUnit'
        ]
        attrsList[2]['attrs']['ou'] = 'group'

        # service dn
        attrsList.append({ 'attrs': {} })
        attrsList[3]['dn'] = 'ou=service,%s' % (self.baseDn)
        attrsList[3]['attrs']['objectclass'] = [
            'top',
            'organizationalUnit'
        ]
        attrsList[3]['attrs']['ou'] = 'service'

        for attrs in attrsList:
            self.add(attrs)

    def createRootUser(self):
        # base dn root
        attrs = { 'attrs': {} }
        attrs['dn'] = 'cn=root,%s' % self.baseDn
        attrs['attrs']['objectclass'] = [
            'organizationalRole'
        ]
        attrs['attrs']['cn'] = 'root'
        attrs['attrs']['description'] = 'root dn user'

        self.add(attrs)

    def run(self):
        args = docopt.docopt(__doc__)

        self.host = raw_input('URL: ')
        self.baseDn = raw_input('Base DN: ')
        self.username = raw_input('Username: ')
        self.password = getpass.getpass('Password: ')
        self.dc = raw_input('DC Name: ')
        self.o = raw_input('Organization: ')

        if args['-v'] == True:
            self.verbose = True

        try:
            self.ldapConn = ldap.initialize(self.host)
            self.ldapConn.simple_bind_s('cn=%s,%s' % (self.username, self.baseDn), self.password)
        except ldap.LDAPError as e:
            print(e)

        self.createBaseDn()
        self.createRootUser()

        self.ldapConn.unbind_s()

if __name__ == '__main__':
    try:
        slappy().run()
    except KeyboardInterrupt as e:
        print('\nInterrupted by User')
