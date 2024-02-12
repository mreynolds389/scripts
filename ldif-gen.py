#!/usr/bin/python3

#
# LDIF file generator
#
# Written by: Mark Reynolds (mreynolds@redhat.com)
#
# Created: 5/20/2014
# Updated: 2/12/2024
#

import sys
import signal
import optparse
import random
from optparse import IndentedHelpFormatter
import textwrap

VERSION = '1.0'
verbose = False
DataDir = "@templatedir@"
padding = True

random_all = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz0123456789_#@%&()?~$^`~*-=+{}|"\'.,<>'
random_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz'
random_alphanum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz0123456789'

#default user attributes
user_attrs = ['description', 'departmentnumber', 'employeeyype', 'homephone', 'initials',
              'telephonenumber', 'facsimiletelephonenumber', 'mobile', 'pager', 'manager',
              'secretary', 'roomnumber', 'carlicense', 'l', 'mail', 'postaladdress'
              'title', 'usercertificate;binary']

# internal list of first and last names in case no "name" files are available
firstnames = ('Adam', 'Alice', 'Brad', 'Brenda', 'Christopher', 'Christine', 'David', 'Diana',
              'Mark', 'Rob', 'Fred', 'Felicia', 'Ludwig', 'George', 'Gloria', 'Hank', 'Heather',
              'Simon', 'Julie', 'Thierry', 'Willie')
lastnames = ('Smith', 'Johnson', 'Bordaz', 'Krispenz', 'Pichugin', 'Reynolds', 'Mosconi',
             'Carter', 'Brown', 'Jenson', 'Mullen', 'Garcia', 'Montbleau', 'Rose', 'Woods',
             'Salinas', 'Sholl', 'Crittenden', 'Dugan', 'Griffith', 'Reynolds', 'Richards', 'Key')
# Misc lists
area_codes = ("303", "415", "408", "510", "804", "818", "213", "206", "714", "610", "650", "512")
seqSet = {}

#
# Org Chart Entries
#
#
# CEO
ceo = {"uid": "ceo", "givenname": "John", "sn": "Budd", "cn": "John Budd", "title": "CEO"}

# Executive Presidents
ep0 = {"uid": "exec_president0", "givenname": "Paul", "sn": "Grant", "cn": "Paul Grant", "title": "Executive President"}
ep1 = {"uid": "exec_president1", "givenname": "Jill", "sn": "Peterson", "cn": "Jill Peterson",
           "title": "Exective President"}
exec_presidents = (ep0, ep1)

# Presidents
p0 = {"uid": "president0", "givenname": "Pete", "sn": "Dunne", "cn": "Pete Dunne", "title": "President"}
p1 = {"uid": "president1", "givenname": "Jannet", "sn": "Keys", "cn": "Jannet Keys", "title": "President"}
p2 = {"uid": "president2", "givenname": "Anne", "sn": "Meissner", "cn": "Anne Meissner", "title": "President"}
presidents = (p0, p1, p2)

# Vice Presidents
vp0 = {"uid": "vice_president0", "givenname": "Jack", "sn": "Cho", "cn": "Jack Cho", "title": "Vice President"}
vp1 = {"uid": "vice_president1", "givenname": "Diane", "sn": "Smith", "cn": "Diane Smith", "title": "Vice President"}
vp2 = {"uid": "vice_president2", "givenname": "Alex", "sn": "Merrells", "cn": "Alex Merrells",
       "title": "Vice President"}
vp3 = {"uid": "vice_president3", "givenname": "Yumi", "sn": "Mehta", "cn": "Yumi Mehta", "title": "Vice President"}
vp4 = {"uid": "vice_president4", "givenname": "Michael", "sn": "Natkovich", "cn": "Michael Natkovich",
       "title": "Vice President"}
vp5 = {"uid": "vice_president5", "givenname": "Keith", "sn": "Lucus", "cn": "Keith Lucus", "title": "Vice President"}
vice_presidents = (vp0, vp1, vp2, vp3, vp4, vp5)

# Directors
d0 = {"uid": "director0", "givenname": "Chris", "sn": "Harrison", "title": "Director", "cn": "Chris Harrison"}
d1 = {"uid": "director1", "givenname": "Jane", "sn": "Baker", "title": "Director", "cn": "Jane Baker"}
d2 = {"uid": "director2", "givenname": "Ed", "sn": "Becket", "title": "Director", "cn": "Ed Becket"}
d3 = {"uid": "director3", "givenname": "Will", "sn": "Stevenson", "title": "Director", "cn": "Will Stevenson"}
d4 = {"uid": "director4", "givenname": "Kieran", "sn": "Beckham", "title": "Director", "cn": "Kieran Beckham"}
d5 = {"uid": "director5", "givenname": "Greg", "sn": "Emerson", "title": "Director", "cn": "Greg Emerson"}
d6 = {"uid": "director6", "givenname": "Ian", "sn": "Parker", "title": "Director", "cn": "Ian Parker"}
d7 = {"uid": "director7", "givenname": "Liem", "sn": "Olson", "title": "Director", "cn": "Liem Olson"}
d8 = {"uid": "director8", "givenname": "George", "sn": "Cruise", "title": "Director", "cn": "George Cruise"}
d9 = {"uid": "director9", "givenname": "Yoshiko", "sn": "Tucker", "title": "Director", "cn": "Yoshiko Tucker"}
directors = (d0, d1, d2, d3, d4, d5, d6, d7, d8, d9)

# Managers
m0 = {'uid': 'manager0', 'givenname': 'Teresa', 'sn': 'Chan', 'cn': 'Teresa Chan', 'title': 'manager'}
m1 = {'uid': 'manager1', 'givenname': 'Tom', 'sn': 'Anderson', 'cn': 'Tom Anderson', 'title': 'manager'}
m2 = {'uid': 'manager2', 'givenname': 'Olga', 'sn': 'Young', 'cn': 'Olga Young', 'title': 'manager'}
m3 = {'uid': 'manager3', 'givenname': 'Bill', 'sn': 'Graham', 'cn': 'Bill Graham', 'title': 'manager'}
m4 = {'uid': 'manager4', 'givenname': 'Todd', 'sn': 'Hoover', 'cn': 'Tom Hoover', 'title': 'manager'}
m5 = {'uid': 'manager5', 'givenname': 'Ken', 'sn': 'Hamilton', 'cn': 'Ken Hamilton', 'title': 'manager'}
m6 = {'uid': 'manager6', 'givenname': 'Christine', 'sn': 'Jobs', 'cn': 'Christine Jobs', 'title': 'manager'}
m7 = {'uid': 'manager7', 'givenname': 'Joanna', 'sn': 'Lake', 'cn': 'Joanna Lake', 'title': 'manager'}
m8 = {'uid': 'manager8', 'givenname': 'Kim', 'sn': 'Remley', 'cn': 'Kim Remley', 'title': 'manager'}
m9 = {'uid': 'manager9', 'givenname': 'Nick', 'sn': 'Pennebaker', 'cn': 'Nick Pennebaker', 'title': 'manager'}
m10 = {'uid': 'manager10', 'givenname': 'Ted', 'sn': 'Hardy', 'cn': 'Ted Hardy', 'title': 'manager'}
m11 = {'uid': 'manager11', 'givenname': 'Tanya', 'sn': 'Nielsen', 'cn': 'Tanya Nielsen', 'title': 'manager'}
m12 = {'uid': 'manager12', 'givenname': 'Sam', 'sn': 'Madams', 'cn': 'Sam Madams', 'title': 'manager'}
m13 = {'uid': 'manager13', 'givenname': 'Judy', 'sn': 'Stewart', 'cn': 'Judy Stewart', 'title': 'manager'}
m14 = {'uid': 'manager14', 'givenname': 'Martha', 'sn': 'Kidman', 'cn': 'Martha Kidman', 'title': 'manager'}
m15 = {'uid': 'manager15', 'givenname': 'Leo', 'sn': 'Knuth', 'cn': 'Leo Knuth', 'title': 'manager'}
m16 = {'uid': 'manager16', 'givenname': 'Cecil', 'sn': 'Guibas', 'cn': 'Cecil Guibas', 'title': 'manager'}
m17 = {'uid': 'manager17', 'givenname': 'Jay', 'sn': 'Hows', 'cn': 'Jay Hows', 'title': 'manager'}
orgManagers = (m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17)

# localities
localities = ("Mountain View", "Redmond", "Redwood Shores", "Armonk", "Cambridge", "Santa Clara",
              "Sunnyvale", "Alameda", "Philadelphia", "Reading", "Cupertino", "Menlo Park", "Palo Alto",
              "Orem", "San Jose", "San Francisco", "Milpitas", "Hartford", "Windsor", "Boston",
              "Westford", "New York", "Detroit", "Austin", "Dallas", "Denver")

# Titles
titles = ("Senior", "Master", "Associate", "Junior", "Chief", "Supreme", "Elite", "Greenhorn")

# Org Units
orgUnits = ('CEO', 'Executive Presidents', 'Presidents', 'Vice Presidents', 'Directors', 'Managers')


def write_org_units(LDIF, suffix):
    for unit in orgUnits:
        LDIF.write('dn: ou=' + unit + ',' + suffix + '\n')
        LDIF.write('objectclass: top\n')
        LDIF.write('objectclass: organizationalUnit\n')
        LDIF.write('ou: ' + unit + '\n')
        LDIF.write('\n')


def write_org_entry(LDIF, suffix, entry):
    LDIF.write('dn: uid=%s,%s\n' % (entry['uid'], suffix))
    LDIF.write('objectclass: top\n')
    LDIF.write('objectclass: person\n')
    LDIF.write('objectclass: inetorgperson\n')
    LDIF.write('objectclass: organizationalPerson\n')
    LDIF.write('uid: ' + entry['uid'] + '\n')
    LDIF.write('cn: ' + entry['cn'] + '\n')
    LDIF.write('sn: ' + entry['sn'] + '\n')
    LDIF.write('givenname: ' + entry['givenname'] + '\n')
    LDIF.write('employeenumber: ' + get_random_value("int", 6) + '\n')
    LDIF.write('homephone: ' + get_random_value("tele") + '\n')
    LDIF.write('initials: ' + str(entry['uid'])[:2] + '\n')
    LDIF.write('telephonenumber: ' + get_random_value("tele") + '\n')
    LDIF.write('facsimiletelephonenumber: ' + get_random_value("tele") + '\n')
    LDIF.write('mobile: ' + get_random_value("tele") + '\n')
    LDIF.write('pager: ' + get_random_value("tele") + '\n')
    LDIF.write('manager: ' + get_manager(entry) + '\n')
    LDIF.write('secretary: ' + get_random_value("secretary") + '\n')
    LDIF.write('roomnumber: ' + get_random_value("int", 5) + '\n')
    LDIF.write('carlicense: ' + get_random_value("alpha", 7) + '\n')
    LDIF.write('l: ' + random_pick(localities) + '\n')
    LDIF.write('mail: ' + get_email_address(entry) + '\n')
    LDIF.write('postaladdress: ' + entry['suffix'] + ' Dept #' + str(random.randomint(1, 25)) + ', Room#' +
               str(random.randomint(1, 1000)) + '\n')
    LDIF.write("usercertificate;binary:: MIIBvjCCASegAwIBAgIBAjANBgkqhkiG9w0BA" +
               "QQFADAnMQ8wDQYD\n VQQDEwZjb25maWcxFDASBgNVBAMTC01NUiBDQSBDZXJ0" +
               "MB4XDTAxMDQwNTE1NTEwNloXDTExMDcw\n NTE1NTEwNlowIzELMAkGA1UEChM" +
               "CZnIxFDASBgNVBAMTC01NUiBTMSBDZXJ0MIGfMA0GCSqGSIb3\n DQEBAQUAA4" +
               "GNADCBiQKBgQDNlmsKEaPD+o3mAUwmW4E40MPs7aiui1YhorST3KzVngMqe5Pb" +
               "ObUH\n MeJN7CLbq9SjXvdB3y2AoVl/s5UkgGz8krmJ8ELfUCU95AQls321RwB" +
               "dLRjioiQ3MGJiFjxwYRIV\n j1CUTuX1y8dC7BWvZ1/EB0yv0QDtp2oVMUeoK9" +
               "/9sQIDAQABMA0GCSqGSIb3DQEBBAUAA4GBADev\n hxY6QyDMK3Mnr7vLGe/HW" +
               "EZCObF+qEo2zWScGH0Q+dAmhkCCkNeHJoqGN4NWjTdnBcGaAr5Y85k1\n o/vO" +
               "AMBsZePbYx4SrywL0b/OkOmQX+mQwieC2IQzvaBRyaNMh309vrF4w5kExReKfj" +
               "R/gXpHiWQz\n GSxC5LeQG4k3IP34\n")
    LDIF.write('\n')


def write_org_chart(LDIF, suffix):
    # Write the organizational units for each org level
    write_org_units(LDIF, suffix)

    # set 'suffix' and 'dnval'
    ceo['suffix'] = suffix
    ceo['dnval'] = ceo['uid']
    write_org_entry(LDIF, 'ou=CEO,' + suffix, ceo)

    for ep in exec_presidents:
        ep['suffix'] = suffix
        ep['dnval'] = ep['uid']
        write_org_entry(LDIF, 'ou=Executive Presidents,' + suffix, ep)

    for p in presidents:
        p['suffix'] = suffix
        p['dnval'] = p['uid']
        write_org_entry(LDIF, 'ou=Presidents,' + suffix, p)

    for vp in vice_presidents:
        vp['suffix'] = suffix
        vp['dnval'] = vp['uid']
        write_org_entry(LDIF, 'ou=Vice Presidents,' + suffix, vp)

    for d in directors:
        d['suffix'] = suffix
        d['dnval'] = d['uid']
        write_org_entry(LDIF, 'ou=Directors,' + suffix, d)

    for m in orgManagers:
        m['suffix'] = suffix
        m['dnval'] = m['uid']
        write_org_entry(LDIF, 'ou=Managers,' + suffix, m)


#
# get_manager
#
def get_manager(user):
    if user['createorgchart']:
        org_idx = random.randint(0, len(orgManagers) - 1)
        dn = ('uid=' + orgManagers[org_idx]['uid'] + ',ou=Managers,' +
              user['suffix'])
        return dn
    else:
        first = firstnames[random.randint(0, len(firstnames) - 1)]
        last = lastnames[random.randint(0, len(lastnames) - 1)]

        return 'uid=' + first[0:1] + last[:] + ',' + user['suffix']


#
# Return an email address based off the user info
#
def get_email_address(user):
    dncomps = user['suffix'].split(',')
    domain = ''
    first = 1
    for val in dncomps:
        val = val.replace(' ', '')
        parts = val.split('=')
        val = parts[1]
        if first:
            domain = domain + val
            first = 0
        else:
            domain = domain + '.'
            domain = domain + val

    return user['dnval'].replace(' ', '.') + '@' + domain


#
# Return a random value of the specified type:
#
# all, alpha, alphanum, int, tele, ssn, secretary
#
def get_random_value(val_type, length=0):
    if length:
        random_len = length
    else:
        random_len = random.randint(10, 30)

    if val_type == 'int':
        if length == 0:
            # get a number that can be long enough to hold a credit number
            length = '9' * 16
        else:
            length = '9' * length
        return str(random.randint(1, int(length)))
    if val_type == 'alpha':
        return (''.join((random.choice(random_alpha)
                for i in range(1, random_len))))
    if val_type == 'alphanum' or val_type == 'all':
        return (''.join((random.choice(random_alphanum)
                for i in range(random_len))))
    if val_type == 'tele':
        areacode = area_codes[random.randint(0, len(area_codes) - 1)]
        prefix = str(random.randint(100, 999))
        postfix = str(random.randint(1000, 9999))
        return "+1 " + areacode + " " + prefix + "-" + postfix
    if val_type == 'ssn':
        one = str(random.randint(0, 900) + 99)
        two = str(random.randint(0, 90) + 9)
        three = str(random.randint(0, 9000) + 999)
        return one + '-' + two + '-' + three
    if val_type == 'secretary':
        return ('cn=' + firstnames[random.randint(0, len(firstnames) - 1)] +
                ' ' + lastnames[random.randint(0, len(lastnames) - 1)])

    return ''.join((random.choice(random_all) for i in xrange(random_len)))


#
# Return a randomly selection value from the provided list of values
#
def random_pick(values):
    val_count = len(values)
    val_count -= 1
    idx = random.randint(0, val_count)
    return values[idx].lstrip()


#
# Maintain a hash (index position) for each attribute we are using seq sets for
#
def seq_pick(attr, values):
    global seqSet

    if attr in seqSet:
        idx = seqSet[attr]
    else:
        seqSet[attr] = 0
        idx = 0

    seqSet[attr] += 1
    if seqSet[attr] >= len(values):
        # reset to the front
        seqSet[attr] = 0

    return values[idx].lstrip()


#
# Open the output LDIF file
#
def open_ldif(file_name):
    file_opened = 0
    LDIF = None
    if file_name:
        if verbose:
            print ('Opening LDIF file: ' + file_name)
        try:
            LDIF = open(file_name, "w")
        except IOError:
            print ("Can't open file: " + file_name)
            exit(1)
    else:
        while file_opened == 0:
            file_name = input('  Enter output LDIF name [/tmp/out.ldif]: ')
            if file_name == '':
                file_name = '/tmp/out.ldif'
            try:
                LDIF = open(file_name, "w")
                file_opened = 1
            except IOError:
                print ("Can\'t open file: " + file_name)
                file_name = ''
    print ('Building LDIF file (%s)...' % file_name)

    return LDIF


#
# Return a number string index
# zero "padding" allow the entry to work with ldclt
#
def get_index(idx, num_users):
    if padding:
        zero_len = len(str(num_users)) - len(str(idx))
        index = '0' * zero_len
        index = index + str(idx)
        return index
    else:
        return idx


#
# Process a list of attribute value pairs.  Check for special keywords, and
# return the dn
#
def process_attr_list(LDIF, value_list, index, mod_list=False):
    dn = ''
    for value_pair in value_list:
        value_pair = value_pair.rstrip()
        if value_pair == '':
            break
        attr_values = value_pair.split(':')
        if len(attr_values) > 1:
            attr = attr_values[0].lower()
            attr_value = attr_values[1].lstrip()
            # attr: RANDOM:int:9
            if attr_value == 'RANDOM':
                # We have a random value, see if the 'type' and 'length' was
                # provided.
                # type: all(default), alpha, int
                # description: RANDOM
                # description: RANDOM:alpha
                # description: RANDOM:alpha:10
                if len(attr_values) == 2:
                    value_pair = attr + ": " + get_random_value("all")
                elif len(attr_values) == 3:
                    value_pair = (attr + ": " +
                                 get_random_value(attr_values[2].lstrip()))
                elif len(attr_values) >= 4:
                    value_pair = (attr + ": " +
                                 get_random_value(attr_values[2].lstrip(),
                                           int(attr_values[3].lstrip())))
            elif attr_value == 'random_pick':
                # Okay we have random values have to gather and select
                if len(attr_values) > 2:
                    values = attr_values[2].split(';')
                    value_pair = attr + ": " + random_pick(values)
            elif attr_value == 'SEQ_SET':
                # Okay we have sequential set values to deal with
                if len(attr_values) > 2:
                    values = attr_values[2].split(';')
                    value_pair = attr + ": " + seq_pick(attr, values)
            if attr in user_attrs:
                user_attrs.remove(attr)
        else:
            print(('Attribute (%s) ' % (attr_values[0])) +
                  'has no delimeter(:) and hence no value. Skipping...')
            continue
        if index:
            value_pair = value_pair.replace('#', str(index))
        if value_pair[0:3] == 'dn:':
            if mod_list:
                LDIF.write('changetype: add\n')
            dn = value_pair

        LDIF.write(value_pair + "\n")
    return dn


#
# Read the tempalte file and store the template in the entry
#
def read_template(entry, member):
    LDIF = None
    if member:
        if verbose:
            print ('Opening template file: ' + entry['member_template_file'])
        try:
            LDIF = open(entry['member_template_file'], "r")
        except IOError:
            print ("Can\'t open template file: " + entry['template_file'])
            exit(1)

        entry['member_template'] = list(LDIF)
    else:
        if verbose:
            print ('Opening template file: ' + entry['template_file'])
        try:
            LDIF = open(entry['template_file'], "r")
        except IOError:
            print ("Can\'t open template file: " + entry['template_file'])
            exit(1)

        entry['template'] = list(LDIF)

    LDIF.close()


#
# Write the group template entries to LDIF
#
def write_group_template(LDIF, idx, group):
    group_index = get_index(idx, group['entries'])
    dn = process_attr_list(LDIF, group['template'], group_index)

    # Add members to the group
    member_idx = 1
    while member_idx <= int(group['members']):
        if 'member_template' in group:
            member_value = \
                group['member_template'][0].rstrip().replace('dn: ', '')
            #member_value = member_value.rstrip()
            if group['create_unique_members']:
                index = ('_' + str(idx) + '_' +
                         get_index(member_idx, group['members']))
            else:
                index = get_index(member_idx, group['members'])
            member_value = member_value.replace('#', index)
            mdn = "%s: %s\n" % (group['member_attr'], member_value)
            LDIF.write(mdn)
        else:
            member_value = group['member_name']
            if group['create_unique_members']:
                member_value = member_value + '_' + str(idx) + '_'
            mdn = "%s: %s=%s%s,%s\n" % (group['member_attr'],
                                        group['member_rdn'],
                                        member_value,
                                        get_index(member_idx, group['members']),
                                        group['member_parent'])
            LDIF.write(mdn)
        if verbose:
            print ('Adding ' + group['member_attr'] + ': ' + member_value +
                   '...')
        member_idx += 1
    if verbose:
        print ('Created group: ' + dn.replace('dn: ', ''))
    LDIF.write('\n')


#
# Write the template entries to LDIF
#
def write_template(LDIF, idx, entry, member=0, member_idx=0, mod_list=False):
    # Start parsing the list
    #
    # Check for key words:  RANDOM, RANDOM-INT
    # Check for selection of random values: RANDOM-PICK: VALUE, VALUE, VALUE
    #
    if member:
        template_entry = entry['member_template']
    else:
        template_entry = entry['template']

    entry_index = get_index(idx, entry['entries'])
    dn = process_attr_list(LDIF, template_entry, entry_index, mod_list)
    LDIF.write('\n')
    if verbose:
        print ('Created entry: ' + dn.replace('dn: ', ''))


def write_parent_entry(LDIF, dn, skip_aci):
    LDIF.write('dn: ' + dn + '\n')
    LDIF.write('objectclass: top\n')

    dn_parts = dn.split('=')
    dn_values = dn_parts[1].split(',')
    if dn_parts[0] == 'o':
        LDIF.write('objectclass: organization\n')
        LDIF.write('o: ' + dn_values[0] + '\n')
    elif dn_parts[0] == 'dc':
        LDIF.write('objectclass: domain\n')
        LDIF.write('dc: ' + dn_values[0] + '\n')
    elif dn_parts[0] == 'ou':
        LDIF.write('objectclass: organizationalUnit\n')
        LDIF.write('ou: ' + dn_values[0] + '\n')
    elif dn_parts[0] == 'cn':
        LDIF.write('objectclass: organizationalUnit\n')
        LDIF.write('ou: ' + dn_values[0] + '\n')
        LDIF.write('cn: ' + dn_values[0] + '\n')
    else:
        LDIF.write('objectclass: extensibleObject\n')
        LDIF.write(dn_parts[0] + ': ' + dn_values[0] + '\n')

    # add a default aci's
    if not skip_aci:
        LDIF.write('aci: (target=ldap:///' + dn + ')(targetattr=*)(version ' +
                   '3.0; acl "Self Write ACI for ' + dn + '"; allow(write) ' +
                   'userdn = "ldap:///self";)\n')
        LDIF.write('aci: (target=ldap:///' + dn + ')(targetattr=*)(version ' +
                   '3.0; acl "Directory Admin ACI for ' + dn +
                   '"; allow(write) groupdn = "ldap:///cn=Directory ' +
                   'Administrators, dc=example,dc=com";)\n')
        LDIF.write('aci: (target=ldap:///' + dn + ')(targetattr=*)(version ' +
                   '3.0; acl "Anonymous ACI for ' + dn + '"; allow(read, ' +
                   'search, compare) userdn = "ldap:///anyone";)\n')

    LDIF.write('\n')
    if verbose:
        print ('Created branch entry: ' + dn)


#
# Write the parent entry, up to and including the base suffix
#
def write_parent(LDIF, parent_dn, suffix_dn, skip_aci, create_chart):
    # do some basic normalization
    parent_dn = parent_dn.replace(' ,', ',')
    parent_dn = parent_dn.replace(', ', ',')
    parent_dn.lower()
    suffix_dn = suffix_dn.replace(' ,', ',')
    suffix_dn = suffix_dn.replace(', ', ',')
    suffix_dn.lower()

    if parent_dn != suffix_dn:
        suffix_parts = suffix_dn.split(',')
        parent_parts = parent_dn.split(',')
        suffix_len = len(suffix_parts)
        parent_len = len(parent_parts)

        position = len(parent_dn) - len(suffix_dn)
        if parent_dn[position:] != suffix_dn:
            print (('The parent DN (%s) and the suffix DN (%s) ' %
                   (parent_dn, suffix_dn)) + 'are not compatible.  ' +
                   'Exiting...')
            LDIF.close()
            exit(1)

        if (parent_len - suffix_len) == 1:
            write_parent_entry(LDIF, suffix_dn, skip_aci)
            if not skip_aci:
                # we only need to write the default ACI's once
                skip_aci = True
        elif (parent_len - suffix_len) > 1:
            # Write the suffix
            write_parent_entry(LDIF, suffix_dn, skip_aci)
            if not skip_aci:
                # we only need to write the default ACI's once
                skip_aci = True

            # Write the filler branches between the suffix and parent DN's
            while True:
                # strip off the top branch
                parent_parts = parent_parts[1:]

                # build the DN
                subsuffix = ''
                for comp in parent_parts:
                    subsuffix = subsuffix + comp + ','

                # remove the last comma
                subsuffix = subsuffix[:-1]
                if subsuffix == suffix_dn:
                    # we're done
                    break
                write_parent_entry(LDIF, subsuffix, True)

        elif suffix_len == parent_len:
            # the dn's are the same length, but do not match!
            print (('The parent DN (%s) and the suffix DN (%s) ' %
                   (parent_dn, suffix_dn)) + 'are not compatible.  ' +
                   'Exiting...')
            LDIF.close()
            exit(1)
        else:
            print ("we should not be here!!")
    write_parent_entry(LDIF, parent_dn, skip_aci)
    if create_chart:
        write_org_chart(LDIF, suffix_dn)


#
# Write the default entry attributes to the LDIF entry
#
def write_user_default_attrs(LDIF, user):
    for attr in user_attrs:
        if attr == 'description':
            LDIF.write(attr + ': Description for ' + user['name'] + '\n')
        elif attr == 'employeenumber':
            LDIF.write(attr + ': ' + get_random_value("int", 6) + '\n')
        elif attr == 'homephone':
            LDIF.write(attr + ': ' + get_random_value("tele") + '\n')
        elif attr == 'initials':
            LDIF.write(attr + ': ' + str(user['uid'])[:2] + '\n')
        elif attr == 'telephonenumber':
            LDIF.write(attr + ': ' + get_random_value("tele") + '\n')
        elif attr == 'facsimiletelephonenumber':
            LDIF.write(attr + ': ' + get_random_value("tele") + '\n')
        elif attr == 'mobile':
            LDIF.write(attr + ': ' + get_random_value("tele") + '\n')
        elif attr == 'pager':
            LDIF.write(attr + ': ' + get_random_value("tele") + '\n')
        elif attr == 'manager':
            LDIF.write(attr + ': ' + get_manager(user) + '\n')
        elif attr == 'secretary':
            LDIF.write(attr + ': ' + get_random_value("secretary") + ',' +
                       user['suffix'] + '\n')
        elif attr == 'roomnumber':
            LDIF.write(attr + ': ' + get_random_value("int", 5) + '\n')
        elif attr == 'carlicense':
            LDIF.write(attr + ': ' + get_random_value("alpha", 7) + '\n')
        elif attr == 'l':
            LDIF.write(attr + ': ' + random_pick(localities) + '\n')
        elif attr == 'mail':
            LDIF.write(attr + ': ' + get_email_address(user) + '\n')
        elif attr == 'postaladdress':
            LDIF.write(attr + ': ' + user['suffix'] + ' Dept #' +
                       str(random.randomint(1, 25)) + ', Room#' +
                       str(random.randomint(1, 1000)) + '\n')
        elif attr == 'title':
            LDIF.write(attr + ': ' + random_pick(titles) + '\n')
        elif attr == 'usercertificate;binary':
            LDIF.write("usercertificate;binary:: MIIBvjCCASegAwIBAgIBAjANBgk" +
                       "qhkiG9w0BAQQFADAnMQ8wDQYD\n VQQDEwZjb25maWcxFDASBgNV" +
                       "BAMTC01NUiBDQSBDZXJ0MB4XDTAxMDQwNTE1NTEwNloXDTExMDcw" +
                       "\n NTE1NTEwNlowIzELMAkGA1UEChMCZnIxFDASBgNVBAMTC01NU" +
                       "iBTMSBDZXJ0MIGfMA0GCSqGSIb3\n DQEBAQUAA4GNADCBiQKBgQ" +
                       "DNlmsKEaPD+o3mAUwmW4E40MPs7aiui1YhorST3KzVngMqe5PbOb" +
                       "UH\n MeJN7CLbq9SjXvdB3y2AoVl/s5UkgGz8krmJ8ELfUCU95AQ" +
                       "ls321RwBdLRjioiQ3MGJiFjxwYRIV\n j1CUTuX1y8dC7BWvZ1/E" +
                       "B0yv0QDtp2oVMUeoK9/9sQIDAQABMA0GCSqGSIb3DQEBBAUAA4GB" +
                       "ADev\n hxY6QyDMK3Mnr7vLGe/HWEZCObF+qEo2zWScGH0Q+dAmh" +
                       "kCCkNeHJoqGN4NWjTdnBcGaAr5Y85k1\n o/vOAMBsZePbYx4Sry" +
                       "wL0b/OkOmQX+mQwieC2IQzvaBRyaNMh309vrF4w5kExReKfjR/gX" +
                       "pHiWQz\n GSxC5LeQG4k3IP34\n")


#
# Build a DN value, make it "unnormalized" if so requested.
# Return the DN and the new rdn value
#
def get_dn(rdn, name, parent, unnorm):
    if unnorm:
        return (rdn.upper() + ' =  ' + name +
                '\"cN=unNormaL, ou=iZED\, z="\,  ,   ' +
                parent), (name + '\"cN=unNormaL, ou=iZED\, z="\,')
    else:
        return (rdn + '=' + name + ',' + parent), name

#
# Get the domain from the suffix
#
def get_domain(suffix):
    dc_parts = suffix.split(',')
    return  '.'.join([part.replace('dc=', '') for part in dc_parts])

#
# Bloat the entry size
#
# If the entry is not are large as the requested size then increase it.
# Use multiple description attributes
#
def bloat_entry(LDIF, final_size):
    curr_size = LDIF.tell()
    if curr_size + 15 < final_size:
        remainder = final_size - curr_size
        while remainder:
            if remainder > 1024:
                LDIF.write('description: ' + get_random_value('alphanum', 1010) +
                           '\n')
                remainder -= 1024
            else:
                LDIF.write('description: ' +
                           get_random_value('alphanum', (remainder - 15)) + '\n')
                remainder = 0

#
# Write IPA User entries to LDIF
#
def write_ipa_users(LDIF, user):
    idx = 1
    user['parent'] = 'cn=users,cn=accounts,' + user['suffix']

    while idx <= int(user['entries']):
        if not user['name']:
            # Use real names
            user['givenname'] = random_pick(firstnames)
            user['sn'] = random_pick(lastnames)
            user['cn'] = user['givenname'] + ' ' + user['sn']
            user['uid'] = user['givenname'][0] + user['sn'] + str(idx)
            user['dnval'] = user['uid']
        else:
            # Use ldclt naming convention
            user['givenname'] = get_random_value("alpha")
            user['sn'] = get_random_value("alpha")
            user['cn'] = user['givenname'] + ' ' + user['sn']
            user['uid'] = user['name'] + get_index(idx, user['entries'])
            user['dnval'] = user['uid']

        (name_dn, rdn) = get_dn('uid', user['dnval'], user['parent'],
                              user['unnorm'])

        # Write the entry
        LDIF.write(f'dn: {name_dn}\n')
        # objectclasses
        LDIF.write('objectclass: top\n')
        LDIF.write('objectclass: person\n')
        LDIF.write('objectclass: inetorgperson\n')
        LDIF.write('objectclass: organizationalPerson\n')
        LDIF.write('objectclass: inetUser\n')
        LDIF.write('objectclass: posixaccount\n')
        LDIF.write('objectclass: krbprincipalaux\n')
        LDIF.write('objectclass: krbticketpolicyaux\n')
        LDIF.write('objectclass: ipaobject\n')
        LDIF.write('objectclass: ipasshuser\n')
        LDIF.write('objectclass: ipaSshGroupOfPubKeys\n')
        LDIF.write('objectclass: mepOriginEntry\n')
        # LDIF.write('objectClass: ipantuserattrs\n')
        # attrs
        LDIF.write(f"uid: {user['uid']}\n")
        LDIF.write(f"cn: {user['cn']}\n")
        LDIF.write(f"sn: {user['sn']}\n")
        LDIF.write(f"givenname: {user['givenname']}\n")
        # posix attrs
        LDIF.write(f"displayName: {user['cn']}\n")
        LDIF.write(f"initials: {str(user['uid'])[:2].upper()}\n")
        LDIF.write(f"gecos: {user['cn']}\n")
        LDIF.write(f"loginShell: /bin/sh\n")
        LDIF.write(f"homeDirectory: /home/{user['uid']}\n")
        LDIF.write(f"uidNumber: {(idx + 1)}\n")
        LDIF.write(f"gidNumber: {(idx + 1)}\n")
        LDIF.write(f"mail: {user['uid']}@{get_domain(user['suffix'])}\n")
        realm = get_domain(user['suffix']).upper()
        LDIF.write(f"krbPrincipalName: {user['uid']}@{realm}\n")
        LDIF.write(f"krbCanonicalName: {user['uid']}@{realm}\n")
        if user['passwd'] == '':
            passwd = user['dnval']
        else:
            passwd = user['passwd']
        LDIF.write(f'userpassword: {passwd}\n')

        # custom values
        process_attr_list(LDIF, user['schema'], idx)

        if verbose:
            print('Created IPA user entry: ' + name_dn)
        LDIF.write('\n')

        idx += 1


#
# Interactive IPA User Entry Creation
#
def create_ipa_users():
    global padding
    user = {
        'schema': [],
        'create_parent': False,
        'createorgchart': False,
        'skip_aci': True,
        'unnorm': False
    }

    print ('\nCreate Users')

    user['entries'] = 'invalid'
    while not user['entries'].isdigit():
        user['entries'] = input('  Number of user entries [10000]: ')
        if user['entries'] == '':
            user['entries'] = '10000'

    user['name'] = input('  Enter user name or press ENTER to use ' +
                         '"real names": ')

    user['passwd'] = input('  Enter userpassword value (default is the ' +
                               'user\'s "uid" value): ')

    user['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if user['suffix'] == '':
        user['suffix'] = 'dc=example,dc=com'

    custom_schema = input('  Add additional attributes [n]: ')
    if custom_schema == 'y':
        print ('    Enter \"attribute: value\", press Enter when finished.  ')
        while True:
            value_pair = input('    Attr/Value: ')
            if value_pair == '':
                break
            user['schema'].append(value_pair)

    user['size'] = 0

    LDIF = open_ldif(None)
    write_ipa_users(LDIF, user)
    LDIF.close()
    print ('Done.')


def write_ipa_hosts(LDIF, host):
    domain_comps = host['fqdn'].split('.')
    hostname = domain_comps.pop(0)
    domain = '.'.join(domain_comps)
    idx = 1
    while idx <= int(host['entries']):
        # Write the entry
        host_name = hostname + str(idx)
        fqdn = f"{host_name}.{domain}"
        LDIF.write(f"dn: fqdn={fqdn},cn=computers,cn=accounts,{host['suffix']}\n")
        LDIF.write('objectClass: top\n')
        LDIF.write('objectClass: ipaobject\n')
        LDIF.write('objectClass: nshost\n')
        LDIF.write('objectClass: ipahost\n')
        LDIF.write('objectClass: ipaservice\n')
        LDIF.write('objectClass: pkiuser\n')
        LDIF.write('objectClass: krbprincipalaux\n')
        LDIF.write('objectClass: krbprincipal\n')
        LDIF.write('objectClass: krbticketpolicyaux\n')
        LDIF.write('objectClass: ipasshhost\n')
        LDIF.write('objectClass: ipaSshGroupOfPubKeys\n')
        LDIF.write(f"fqdn: {fqdn}\n")
        LDIF.write(f"cn: {fqdn}\n")
        LDIF.write(f"serverHostName: {host_name}\n")
        realm = get_domain(host['suffix']).upper()
        LDIF.write(f"krbPrincipalName: host/{fqdn}@{realm}\n")
        LDIF.write(f"krbCanonicalName: host/{fqdn}@{realm}\n")
        # process custom attributes
        process_attr_list(LDIF, host['schema'], idx)

        if verbose:
            print('Created host entry: ' + name_dn)
        LDIF.write('\n')
        idx += 1


def create_ipa_hosts():
    print('\nCreate Users')
    host = {
        'schema': [],
        'entries': 'invalid'
    }
    while not host['entries'].isdigit():
        host['entries'] = input('  Number of host entries [1000]: ')
        if host['entries'] == '':
            host['entries'] = '1000'

    host['fqdn'] = input('  Enter FQDN: ')

    host['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if host['suffix'] == '':
        host['suffix'] = 'dc=example,dc=com'

    custom_schema = input('  Add additional attributes [n]: ')
    if custom_schema == 'y':
        print ('    Enter \"attribute: value\", press Enter when finished.  ')
        while True:
            value_pair = input('    Attr/Value: ')
            if value_pair == '':
                break
            host['schema'].append(value_pair)

    LDIF = open_ldif(None)
    write_ipa_hosts(LDIF, host)
    LDIF.close()
    print ('Done.')


#
# Write user entries to LDIF
#
def write_users(LDIF, user, mod_list=False):
    idx = 1

    if user['create_parent']:
        write_parent(LDIF, user['parent'], user['suffix'], user['skip_aci'],
                    user['createorgchart'])

    while idx <= int(user['entries']):
        if 'template' in user:
            write_template(LDIF, idx, user, 0, 0, mod_list)
        else:
            print_rdn = False
            if not user['name']:
                # Use real names
                user['givenname'] = random_pick(firstnames)
                user['sn'] = random_pick(lastnames)
                user['cn'] = user['givenname'] + ' ' + user['sn']
                user['uid'] = str(user['givenname'])[:1] + str(user['sn'])[:]
                if user['rdn'] == 'cn':
                    user['cn'] = user['cn'] + str(idx)
                    user['dnval'] = user['cn']
                elif user['rdn'] == 'uid':
                    user['uid'] = user['uid'] + str(idx)
                    user['dnval'] = user['uid']
                else:
                    print_rdn = True
                    user['dnval'] = user['uid'] + str(idx)
            else:
                # Use ldclt naming convention
                user['givenname'] = get_random_value("alpha")
                user['sn'] = get_random_value("alpha")
                user['cn'] = user['givenname'] + ' ' + user['sn']
                user['uid'] = user['name'] + get_index(idx, user['entries'])
                if user['rdn'] == 'cn':
                    user['cn'] = user['cn'] + get_index(idx, user['entries'])
                    user['dnval'] = user['cn']
                elif user['rdn'] == 'uid':
                    user['dnval'] = user['uid']
                else:
                    print_rdn = True
                    user['dnval'] = user['uid'] + str(idx)

            (name_dn, rdn) = get_dn(user['rdn'], user['dnval'], user['parent'],
                                  user['unnorm'])
            if user['rdn'] == 'cn':
                    user['cn'] = rdn
            elif user['rdn'] == 'uid':
                    user['uid'] = rdn

            # Write the entry
            LDIF.write('dn: ' + name_dn + '\n')
            if mod_list:
                LDIF.write('changetype: add\n')
            LDIF.write('objectclass: top\n')
            LDIF.write('objectclass: person\n')
            LDIF.write('objectclass: inetorgperson\n')
            LDIF.write('objectclass: organizationalPerson\n')
            LDIF.write('objectclass: inetUser\n')
            if print_rdn:
                LDIF.write(user['rdn'] + ": " + rdn + '\n')
            LDIF.write('uid: ' + user['uid'] + '\n')
            LDIF.write('cn: ' + user['cn'] + '\n')
            LDIF.write('sn: ' + user['sn'] + '\n')
            LDIF.write('givenname: ' + user['givenname'] + '\n')
            process_attr_list(LDIF, user['schema'], idx)

            # write the remaining default attribute
            write_user_default_attrs(LDIF, user)
            if user['passwd'] == '':
                passwd = user['dnval']
            else:
                passwd = user['passwd']
            LDIF.write('userpassword: ' + passwd + '\n')

            # bloat the entry size if requested
            if user['size']:
                bloat_entry(LDIF, int(user['size']))

            if verbose:
                print ('Created user entry: ' + name_dn)
            LDIF.write('\n')

        idx += 1


#
# Interactive User Entry Creation
#
def create_users():
    global padding
    user = {
        'schema': [],
        'create_parent': False,
        'createorgchart': False,
        'skip_aci': True,
        'unnorm': False
    }

    print ('\nCreate Users')

    user['entries'] = 'invalid'
    while not user['entries'].isdigit():
        user['entries'] = input('  Number of user entries [10000]: ')
        if user['entries'] == '':
            user['entries'] = '10000'

    pad = input('  Zero pad the user name index(for ldclt)[y]: ')
    if pad == 'n':
        padding = False

    user['rdn'] = input('  Enter the RDN Attribute [uid]: ')
    if user['rdn'] == '':
        user['rdn'] = "uid"

    user['name'] = input('  Enter user name or press ENTER to use ' +
                             '"real names": ')

    answer = input('  Use unnormalized DN\'s [n]: ')
    if answer == 'y':
        user['unnorm'] = True

    user['passwd'] = input('  Enter userpassword value (default is the ' +
                               'user\'s "uid" value): ')

    user['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if user['suffix'] == '':
        user['suffix'] = 'dc=example,dc=com'

    user['parent'] = input('  Enter parent DN [' + user['suffix'] + ']: ')
    if user['parent'] == '':
        user['parent'] = user['suffix']

    answer = input('  Create parent entry [n]: ')
    if answer == 'y':
        user['create_parent'] = True
        answer = input('  Add default ACI\'s to parent entry [y]: ')
        if answer == 'y':
            user['skip_aci'] = False

    answer = input('  Create organization chart [n]: ')
    if answer == 'y':
        user['createorgchart'] = True
        user['create_parent'] = True

    custom_schema = input('  Add additional attributes [n]: ')
    if custom_schema == 'y':
        print ('    Enter \"attribute: value\", press Enter when finished.  ')
        while True:
            value_pair = input('    Attr/Value: ')
            if value_pair == '':
                break
            user['schema'].append(value_pair)

    user['size'] = -1
    while user['size'] < 0:
        user['size'] = int(input('  Enter entry size(in bytes) or press ' +
                                 'ENTER for default size: '))
        if user['size'] == '':
            user['size'] = 0
            break

    LDIF = open_ldif(None)
    write_users(LDIF, user)
    LDIF.close()
    print ('Done.')


def write_nested(LDIF, user):
    entry_pool = int(user['entries'])
    entry_count = 0
    cont_count = 0;

    if user['create_parent']:
        write_parent(LDIF, user['suffix'], user['suffix'], user['skip_aci'],
                    user['createorgchart'])

    while entry_count < entry_pool:
        cont_count += 1

        # Create container
        container_dn = 'cn=container' + str(cont_count) + ',' + user['suffix']
        LDIF.write('dn: ' + container_dn + '\n')
        LDIF.write('objectclass: top\n')
        LDIF.write('objectclass: nsContainer\n')
        LDIF.write('cn: container' + str(cont_count) + '\n\n')
        entry_count += 1

        for i in range(1, 10):
            if entry_count >= entry_pool:
                break
            # Create sub container
            container_dn = 'cn=container' + str(i) + ',' + container_dn
            LDIF.write('dn: ' + container_dn + '\n')
            LDIF.write('objectclass: top\n')
            LDIF.write('objectclass: nsContainer\n')
            LDIF.write('cn: container' + str(cont_count) + '\n\n')
            entry_count += 1

            for idx in range(1, 1000):
                if entry_count >= entry_pool:
                    break
                if not user['name']:
                    # Use real names
                    user['givenname'] = random_pick(firstnames)
                    user['sn'] = random_pick(lastnames)
                    user['cn'] = user['givenname'] + ' ' + user['sn']
                    user['uid'] = str(user['givenname'])[:1] + str(user['sn'])[:]
                    if user['rdn'] == 'cn':
                        user['cn'] = user['cn'] + str(idx)
                        user['dnval'] = user['cn']
                    elif user['rdn'] == 'uid':
                        user['uid'] = user['uid'] + str(idx)
                        user['dnval'] = user['uid']
                    else:
                        user['dnval'] = user['uid'] + str(idx)
                else:
                    # Use ldclt naming convention
                    user['givenname'] = get_random_value("alpha")
                    user['sn'] = get_random_value("alpha")
                    user['cn'] = user['givenname'] + ' ' + user['sn']
                    user['uid'] = user['name'] + get_index(idx, user['entries'])
                    if user['rdn'] == 'cn':
                        user['cn'] = user['cn'] + get_index(idx, user['entries'])
                        user['dnval'] = user['cn']
                    elif user['rdn'] == 'uid':
                        user['dnval'] = user['uid']
                    else:
                        user['dnval'] = user['uid'] + str(idx)

                (name_dn, rdn) = get_dn(user['rdn'], user['dnval'], container_dn,
                                      user['unnorm'])
                if user['rdn'] == 'cn':
                        user['cn'] = rdn
                elif user['rdn'] == 'uid':
                        user['uid'] = rdn

                LDIF.write('dn: ' + name_dn + '\n')
                LDIF.write('objectclass: top\n')
                LDIF.write('objectclass: person\n')
                LDIF.write('objectclass: inetorgperson\n')
                LDIF.write('objectclass: organizationalPerson\n')
                LDIF.write('objectclass: inetUser\n')
                LDIF.write('uid: ' + user['uid'] + '\n')
                LDIF.write('cn: ' + user['cn'] + '\n')
                LDIF.write('sn: ' + user['sn'] + '\n')
                LDIF.write('givenname: ' + user['givenname'] + '\n')
                write_user_default_attrs(LDIF, user)
                LDIF.write('\n')

                entry_count += 1
    print("Created {} entries...".format(entry_count))


def create_nested_ldif():
    global padding
    user = {
        'schema': [],
        'create_parent': True,
        'createorgchart': False,
        'skip_aci': True,
        'unnorm': False,
        'size': 0
    }

    print ('\nCreate Users')

    user['entries'] = 'invalid'
    while not user['entries'].isdigit():
        user['entries'] = input('  Number of user entries [100000]: ')
        if user['entries'] == '':
            user['entries'] = '100000'

    pad = input('  Zero pad the user name index(for ldclt)[y]: ')
    if pad == 'n':
        padding = False

    user['rdn'] = input('  Enter the RDN Attribute [uid]: ')
    if user['rdn'] == '':
        user['rdn'] = "uid"

    user['name'] = input('  Enter user name or press ENTER to use ' +
                             '"real names": ')

    user['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if user['suffix'] == '':
        user['suffix'] = 'dc=example,dc=com'

    LDIF = open_ldif(None)
    write_nested(LDIF, user)
    LDIF.close()
    print ('Done.')


#
# Write group entries and members to LDIF
#
def write_group(LDIF, group):
    idx = 1
    member_idx = 1
    wrote_aci = 0

    if LDIF is None:
        LDIF = open_ldif(None)

    if group['create_parent']:
        write_parent(LDIF, group['parent'], group['suffix'], group['skip_aci'],
                    False)
        wrote_aci = 1
    if group['member_parent'] != group['parent'] and \
       group['create_member_parent']:
        if wrote_aci:
            write_parent(LDIF, group['member_parent'], group['suffix'], True,
                        False)
        else:
            write_parent(LDIF, group['member_parent'], group['suffix'],
                        group['skip_aci'], False)

    # Now we create the same members
    if not group['create_unique_members']:
        if not 'member_template' in group:
            if group['create_members']:
                user = {
                    'suffix': group['suffix'],
                    'schema': group['member_schema'],
                    'name': group['member_name'],
                    'parent': group['member_parent'],
                    'rdn': group['member_rdn'],
                    'passwd': group['member_passwd'],
                    'entries': group['members'],
                    'unnorm': False,
                    'createorgchart': False,
                    'size': 0,
                    'create_parent': False
                }
                write_users(LDIF, user)
        else:
            # member template supplied, so we assume we want to create members
            while member_idx <= int(group['members']):
                write_template(LDIF, member_idx, group, 1)
                member_idx += 1
            LDIF.write('\n')

    while idx <= int(group['entries']):
        # Create the users on each group pass since members are unique
        if group['create_unique_members']:
            if 'member_template' in group:
                # use the template
                member_idx = 1
                while member_idx <= int(group['members']):
                    write_template(LDIF, member_idx, group, 1, idx)
                    member_idx += 1
            else:
                if group['create_members'] or group['create_unique_members']:
                    user = {'schema': group['member_schema']}
                    if group['create_unique_members']:
                        user['name'] = (group['member_name'] + '_' + str(idx) +
                                        '_')
                    else:
                        user['name'] = group['member_name']
                    user['parent'] = group['member_parent']
                    user['rdn'] = group['member_rdn']
                    user['passwd'] = group['member_passwd']
                    user['entries'] = group['members']
                    user['unnorm'] = False
                    user['createorgchart'] = False
                    user['size'] = 0
                    user['create_parent'] = False  # This was done above
                    user['suffix'] = group['suffix']
                    write_users(LDIF, user)
            LDIF.write('\n')

        if 'template' in group:
            write_group_template(LDIF, idx, group)
        else:
            member_idx = 1
            group_value = group['name'] + get_index(idx, group['entries'])
            rdn_value = group['rdn'] + '=' + group_value
            name_dn = rdn_value + ',' + group['parent']

            LDIF.write('dn: ' + name_dn + '\n')
            LDIF.write('objectclass: top\n')
            LDIF.write('objectclass: groupOfUniqueNames\n')
            LDIF.write('objectclass: groupOfNames\n')
            if group['rdn'] != "cn":
                LDIF.write('cn: ' + get_random_value("alpha") + '\n')
            LDIF.write(group['rdn'] + ": " + group_value + '\n')
            process_attr_list(LDIF, group['schema'], idx)

            # Add members
            while member_idx <= int(group['members']):
                name = group['member_name']
                if group['create_unique_members']:
                    name = group['member_name'] + '_' + str(idx) + '_'
                mdn = ("%s=%s%s,%s" % (group['member_rdn'], name,
                                       get_index(member_idx, group['members']),
                                       group['member_parent']))
                if verbose:
                    print ('Adding ' + group['member_attr'] + ': ' + mdn)
                LDIF.write("%s: %s\n" % (group['member_attr'], mdn))
                member_idx += 1
            LDIF.write('\n')
            if verbose:
                print ('Created group: ' + name_dn)

        idx += 1

    LDIF.close()
    print ("Done.")


#
# Interactive Group Creation
#
def create_group():
    global padding
    group = {
        'schema': [],
        'member_schema': [],
        'create_members': False,
        'create_member_parent': False,
        'create_parent': False,
        'create_unique_members': False,
        'skip_aci': True
    }

    print ('\nCreate Groups')

    group['entries'] = 'invalid'
    while not group['entries'].isdigit():
        group['entries'] = input('  Number of group entries [1]: ')
        if group['entries'] == '':
            group['entries'] = '1'

    pad = input('  Zero pad the group name index(for ldclt)[y]: ')
    if pad == 'n':
        padding = False

    group['rdn'] = input('  Enter the RDN Attribute [cn]: ')
    if group['rdn'] == '':
        group['rdn'] = "cn"

    group['name'] = input('  Enter base user name [group_entry]: ')
    if group['name'] == '':
        group['name'] = 'group_entry'

    group['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if group['suffix'] == '':
        group['suffix'] = 'dc=example,dc=com'

    group['parent'] = input('  Enter parent DN [' +
                                group['suffix'] + ']: ')
    if group['parent'] == '':
        group['parent'] = group['suffix']

    answer = input('  Create parent entry [n]: ')
    if answer == 'y':
        group['create_parent'] = True
        answer = input('  Add default ACI\'s to parent entry [y]: ')
        if answer == '' or answer == 'y':
            group['skip_aci'] = False

    group['member_attr'] = input('  Enter the membership attribute ' +
                                     '[uniqueMember]: ')
    if group['member_attr'] == '':
        group['member_attr'] = 'uniqueMember'

    custom_schema = input('  Add additional attributes [n]: ')
    if custom_schema == 'y':
        print ('    Enter \"attribute: value\", press Enter when finished.')
        while True:
            value_pair = input('    Attr/Value: ')
            if value_pair == '':
                break
            group['schema'].append(value_pair)

    group['members'] = input('  Enter the number of members [10000]: ')
    if group['members'] == '':
        group['members'] = '10000'

    if int(group['members']) > 0:
        group['member_parent'] = input('  Enter the member parent [' +
                                           group['parent'] + ']: ')
        if group['member_parent'] == '':
            group['member_parent'] = group['parent']

        group['member_rdn'] = input('  Enter member entry rdn [uid]: ')
        if group['member_rdn'] == '':
            group['member_rdn'] = 'uid'

        group['member_name'] = input('  Enter member name or press ' +
                                         'ENTER to use "real names": ')

        answer = input('  Create unique members across all the groups ' +
                           '[n]: ')
        if answer == 'y':
            group['create_unique_members'] = True

        answer = input('  Create the member entries [n]: ')
        if answer == 'y':
            group['create_members'] = True
            template = input('  Do you want to use a template file [n]: ')
            if template == 'y':
                group['member_template_file'] = ''
                while group['member_template_file'] == '':
                    group['member_template_file'] = \
                        input('  Enter template file name: ')
                read_template(group, 1)
            else:
                answer = input('  Create member parent entry [n]: ')
                if answer == 'y':
                    group['create_member_parent'] = True

                group['member_passwd'] = \
                    input('  Enter member\'s userpassword value ' +
                              '(default is the member\'s "uid" value): ')

                custom_schema = input('  Add additional attributes to ' +
                                         'member entry [n]: ')
                if custom_schema == 'y':
                    print ('    Enter \"attribute: value\", press Enter ' +
                           'when finished.')
                    while True:
                        value_pair = input('    Attr/Value: ')
                        if value_pair == '':
                            break
                        group['member_schema'].append(value_pair)
        else:
            group['create_members'] = False
    write_group(None, group)


#
# Write the organizational units to LDIF
#
def write_ou(LDIF, ou):
    idx = 1
    if LDIF is None:
        LDIF = open_ldif(None)

    if ou['create_parent']:
        write_parent(LDIF, ou['parent'], ou['suffix'], ou['skip_aci'], False)

    while idx <= int(ou['entries']):
        if 'template' in ou:
            write_template(LDIF, idx, ou)
        else:
            ou_value = ou['name'] + get_index(idx, ou['entries'])
            rdn_value = ou['rdn'] + '=' + ou_value
            name_dn = rdn_value + ',' + ou['parent']

            LDIF.write('dn: ' + name_dn + '\n')
            LDIF.write('objectclass: top\n')
            LDIF.write('objectclass: organizationalUnit\n')
            if ou['rdn'] != "ou":
                LDIF.write('ou: ' + ou_value + '\n')
            LDIF.write(ou['rdn'] + ": " + ou_value + '\n')
            process_attr_list(LDIF, ou['schema'], idx)
            LDIF.write('\n')
            if verbose:
                print ('Created organizational unit: ' + name_dn)

        idx += 1

    LDIF.close()
    print ('Done.')


#
# Interactive Organization Unit Creation
#
def create_ou():
    global padding
    ou = {
        'schema': [],
        'create_parent': False,
        'skip_aci': True
    }

    print ('\nCreate Orgnaizational Units')

    ou['entries'] = 'invalid'
    while not ou['entries'].isdigit():
        ou['entries'] = input('  Number of organizational unit entries ' +
                                  '[1]: ')
        if ou['entries'] == '':
            ou['entries'] = '1'

    pad = input('  Zero pad the organizational unit name index' +
                    '(for ldclt)[y]: ')
    if pad == 'n':
        padding = False

    ou['rdn'] = input('  Enter the RDN Attribute [ou]: ')
    if ou['rdn'] == '':
        ou['rdn'] = "ou"

    ou['name'] = input('  Enter organizational unit [my_ou]: ')
    if ou['name'] == '':
        ou['name'] = 'my_ou'

    ou['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if ou['suffix'] == '':
        ou['suffix'] = 'dc=example,dc=com'

    ou['parent'] = input('  Enter entry parent DN [' +
                             ou['suffix'] + ']: ')
    if ou['parent'] == '':
        ou['parent'] = ou['suffix']

    answer = input('  Create parent entry [n]: ')
    if answer == 'y':
        ou['create_parent'] = True
        answer = input('  Add default ACI\'s to parent entry [y]: ')
        if answer == '':
            ou['skip_aci'] = False

    custom_schema = input('  Add additional attributes [n]: ')
    if custom_schema == 'y':
        print ('    Enter \"attribute: value\", press Enter when finished.  ')
        while True:
            value_pair = input('    Attr/Value: ')
            if value_pair == '':
                break
            ou['schema'].append(value_pair)

    write_ou(None, ou)


#
# Write the Bad LDIF
#
def write_bad_ldif(blended, entries):
    idx = 1
    LDIF = open_ldif(None)

    write_parent(LDIF, "dc=example,dc=com", "dc=example,dc=com", True, False)

    while idx <= int(entries):
        ou_value = 'myDups' + get_index(idx, entries)
        LDIF.write('dn: ou=' + ou_value + ',dc=example,dc=com\n')
        LDIF.write('objectclass: top\n')
        LDIF.write('objectclass: organizationalUnit\n')
        LDIF.write('ou: ' + ou_value + '\n')
        LDIF.write('\n')

        if blended:
            # Add it again
            ou_value = 'myDups' + get_index(idx, entries)
            LDIF.write('dn: ou=' + ou_value + ',dc=example,dc=com\n')
            LDIF.write('objectclass: top\n')
            LDIF.write('objectclass: organizationalUnit\n')
            LDIF.write('ou: ' + ou_value + '\n')
            LDIF.write('\n')

        idx += 1

    if not blended:
        # Add the dups at the end
        idx = 1
        while idx <= int(entries):
            ou_value = 'myDups' + get_index(idx, entries)
            LDIF.write('dn: ou=' + ou_value + ',dc=example,dc=com\n')
            LDIF.write('objectclass: top\n')
            LDIF.write('objectclass: organizationalUnit\n')
            LDIF.write('ou: ' + ou_value + '\n')
            LDIF.write('\n')
            idx += 1

    LDIF.close()
    print ('Done.')


#
# Interactive Bad LDIF Creation
#
def create_bad_ldif():
    print ('\nCreate Bad Ldif')

    entries = "zero"
    while not entries.isdigit():
        entries = input('  Number of entries [10000]: ')
        if entries == '':
            entries = '10000'

    choice = input('  Duplicate DNs [0]: ')
    if choice == '' or choice.lower() == 'yes' or choice.lower() == 'y':
        choice = input('  Blended [yes] ')
        blend = False
        if choice == '' or choice.lower() == 'yes' or choice.lower() == 'y':
            blend = True
        write_bad_ldif(blend, entries)


#
# Write the Role entries to LDIF
#
def write_role(LDIF, role):
    objectclasses = ''
    if role['role_type'] == 'managed':
        objectclasses = ('objectclass: nsSimpleRoleDefinition\nobjectclass: ' +
                         'nsManagedRoleDefinition\n')
    elif role['role_type'] == 'filtered':
        objectclasses = ('objectclass: nsComplexRoleDefinition\nobjectclass:' +
                         ' nsFilteredRoleDefinition\n')
    elif role['role_type'] == 'nested':
        objectclasses = ('objectclass: nsComplexRoleDefinition\nobjectclass:' +
                         ' nsNestedRoleDefinition\n')

    if LDIF is None:
        LDIF = open_ldif(None)

    if role['create_parent']:
        write_parent(LDIF, role['parent'], role['suffix'], role['skip_aci'],
                    False)

    idx = 1
    while idx <= int(role['entries']):
        if 'template' in role:
            write_template(LDIF, idx, role)
        else:
            dn = ('dn: cn=%s%s,%s\n' % (role['name'],
                                        get_index(idx,
                                        role['entries']),
                                        role['parent']))
            LDIF.write(dn)
            LDIF.write('objectclass: top\n')
            LDIF.write('objectclass: LdapSubEntry\n')
            LDIF.write('objectclass: nsRoleDefinition\n')
            LDIF.write(objectclasses)
            if role['role_type'] == 'nested':
                for value in role['role_list']:
                    #
                    # check for RANDOM_PICK and SEQ_SET
                    #
                    pair = value.split(':')
                    if len(pair) > 1:
                        attr_value = pair[0].lstrip()
                        if attr_value == 'RANDOM_PICK':
                            values = pair[1].split(';')
                            value = random_pick(values)
                        elif attr_value == 'SEQ_SET':
                            values = pair[1].split(';')
                            value = seq_pick("nsRoleDN", values)
                    LDIF.write('nsRoleDN: ' + value + '\n')

            if role['role_type'] == 'filtered':
                value = role['filter']
                pair = value.split(':')
                if len(pair) > 1:
                    attr_value = pair[0].lstrip()
                    if attr_value == 'RANDOM_PICK':
                        values = pair[1].split(';')
                        value = random_pick(values)
                    elif attr_value == 'SEQ_SET':
                        values = pair[1].split(';')
                        value = seq_pick("nsRoleFilter", values)
                LDIF.write('nsRoleFilter: ' + value + '\n')

            LDIF.write('cn: ' + role['name'] + get_index(idx, role['entries']) +
                       '\n')
            LDIF.write('\n')
            if verbose:
                print ('Created role: ' + dn.rstrip())
            idx += 1

    LDIF.close()
    print ('Done.')


#
# Interactive Role Creation
#
def create_role(role_type):
    role = {
        'role_list': [],
        'create_parent': False,
        'skip_aci': True
    }

    print ('\nCreate ' + role_type + ' role')

    role['entries'] = input('  Enter number of roles to create [1]: ')
    if role['entries'] == '':
        role['entries'] = '1'

    role['name'] = input('  Enter Role Name [myRole]: ')
    if role['name'] == '':
        role['name'] = 'myRole'

    role['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if role['suffix'] == '':
        role['suffix'] = 'dc=example,dc=com'

    role['parent'] = input('  Enter entry parent DN [' + role['suffix'] +
                               ']: ')
    if role['parent'] == '':
        role['parent'] = role['suffix']

    answer = input('  Create parent entry [n]: ')
    if answer == 'y':
        role['create_parent'] = True
        answer = input('  Add default ACI\'s to parent entry [y]: ')
        if answer == '' or answer == 'y':
            role['skip_aci'] = False

    if role_type == 'nested':
        print ('  Add nsRoleDNs (press Enter when finished)')
        while True:
            value = input('  nsRoleDN: ')
            if value == '':
                break
            role['role_list'].append(value)

    if role_type == 'filtered':
        role['filter'] = input('  Enter role filter [objectclass=top]: ')
        if role['filter'] == '':
            role['filter'] = 'objectclass=top'

    print ('\n')
    write_role(None, role)


#
# Write the COS entries to the LDIF
#
def write_cos(LDIF, cos_type, cos_template, cos_def):
    objectclass = ''
    if cos_type == 'pointer':
        objectclass = 'objectclass: cosPointerDefinition\n'
    if cos_type == 'indirect':
        objectclass = 'objectclass: cosIndirectDefinition\n'
    if cos_type == 'classic':
        objectclass = 'objectclass: cosClassicDefinition\n'

    if LDIF is None:
        LDIF = open_ldif(None)

    if cos_template['create_parent']:
        write_parent(LDIF, cos_template['parent'], cos_template['suffix'], True, False)
    if cos_def['create_parent'] and cos_template['parent'] != cos_def['parent']:
        write_parent(LDIF, cos_def['parent'], cos_def['suffix'], True, False)

    idx = 1
    while idx <= int(cos_def['entries']):
        # Create definition entry
        dn = ('dn: cn=%s%s,%s\n' % (cos_def['name'],
                                    get_index(idx, int(cos_def['entries'])),
                                    cos_def['parent']))
        LDIF.write(dn)
        LDIF.write('objectclass: top\n')
        LDIF.write('objectclass: cosSuperDefinition\n')
        LDIF.write(objectclass)
        LDIF.write('cn: ' + cos_def['name'] +
                   get_index(idx, int(cos_def['entries'])) + '\n')

        if cos_type == 'pointer' or cos_type == 'classic':
            LDIF.write('cosTemplateDN: cn=' + cos_template['name'] +
                       get_index(idx, int(cos_def['entries'])) +
                       ',' + cos_template['parent'] + '\n')
        if cos_type == 'classic':
            value = cos_def['cosSpecifier']
            pair = value.split(':')
            if len(pair) > 1:
                attr_value = pair[0].lstrip()
                if attr_value == 'RANDOM_PICK':
                    values = pair[1].split(';')
                    value = random_pick(values)
                elif attr_value == 'SEQ_SET':
                    if len(pair) > 1:
                        values = pair[1].split(';')
                        value = seq_pick("cosSpecifier", values)
            LDIF.write('cosSpecifier: ' + value + '\n')

        if cos_type == 'indirect':
            value = cos_def['indirectSpecifier']
            pair = value.split(':')
            if len(pair) > 1:
                attr_value = pair[0].lstrip()
                if attr_value == 'RANDOM_PICK':
                    values = pair[1].split(';')
                    value = random_pick(values)
                elif attr_value == 'SEQ_SET':
                    values = pair[1].split(';')
                    value = seq_pick("cosIndirectSpecifier", values)
            LDIF.write('cosIndirectSpecifier: ' + value + '\n')

        for attr in cos_def['attr_list']:
            value = attr
            pair = attr.split(':')
            if len(pair) > 1:
                attr_value = pair[0].lstrip()
                if attr_value == 'RANDOM_PICK':
                    values = pair[1].split(';')
                    value = random_pick(values)
                elif attr_value == 'SEQ_SET':
                    values = pair[1].split(';')
                    value = seq_pick("cosAttribute", values)
            LDIF.write('cosAttribute: ' + value + '\n')

        LDIF.write('\n')
        if verbose:
            print ('Created COS defintion entry: ' + dn.rstrip())
        idx += 1

    idx = 1
    while idx <= int(cos_template['entries']) and int(cos_template['entries']) > 0:
        # Create template entry
        dn = 'dn: cn=' + cos_template['name'] + get_index(idx, int(cos_def['entries'])) + ',' + cos_template['parent'] + '\n'
        LDIF.write(dn)
        LDIF.write('objectclass: top\n')
        LDIF.write('objectclass: extensibleObject\n')
        LDIF.write('objectclass: cosTemplate\n')
        LDIF.write('cn: ' + cos_template['name'] + get_index(idx, int(cos_def['entries'])) + '\n')
        for attr in cos_template['attr_list']:
            value = attr
            pair = attr.split(':')
            if len(pair) > 2:
                attr_value = pair[1].lstrip()
                if attr_value == 'RANDOM_PICK':
                    values = pair[2].split(';')
                    value = pair[0] + ': ' + random_pick(values)
                elif attr_value == 'SEQ_SET':
                    values = pair[2].split(';')
                    value = pair[0] + ': ' + seq_pick(pair[0], values)
            LDIF.write(value + '\n')
        LDIF.write('cosPriority: ' + cos_template['priority'] + '\n')
        LDIF.write('\n')
        if verbose:
            print ('Created DOS template entry: ' + dn.rstrip())
        idx += 1

    LDIF.close()
    print ("Done.")


#
# Interactive COS Creation
#
def create_cos(cos_type):
    cos_template = {
        'attr_list': [],
        'create_parent': False,
        'skip_aci': True
    }
    cos_def = {
        'attr_list': [],
        'create_parent': False,
        'skip_aci': True
    }

    print ('\nCreate COS (' + cos_type + ')')

    cos_template['entries'] = input('  Enter the number of COS templates to create [1]: ')
    if cos_template['entries'] == '':
        cos_template['entries'] = '1'

    cos_template['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if cos_template['suffix'] == '':
        cos_template['suffix'] = 'dc=example,dc=com'

    if cos_template['entries'] > 0:
        # indirect COS does not use a template, so its okay to skip the template questions
        cos_template['name'] = input('  Enter COS Template Name [cosTemplate]: ')
        if cos_template['name'] == '':
            cos_template['name'] = 'cosTemplate'

        cos_template['parent'] = input('  Enter template parent DN [' + cos_template['suffix'] + ']: ')
        if cos_template['parent'] == '':
            cos_template['parent'] = cos_template['suffix']

        answer = input('  Create template parent entry [n]: ')
        if answer == 'y':
            cos_template['create_parent'] = True
            answer = input('  Add default ACI\'s to parent entry [y]: ')
            if answer == '' or answer == 'y':
                cos_template['skip_aci'] = False

        print ('  Enter template \"attribute: value\", press Enter when finished.')
        while True:
            value_pair = input('  Attr/Value: ')
            if value_pair == '':
                break
            cos_template['attr_list'].append(value_pair)
        cos_template['priority'] = input('  Enter template priority [0]: ')
        if cos_template['priority'] == '':
            cos_template['priority'] = '0'

    cos_def['entries'] = input('  Enter the number of COS defintions to create [1]: ')
    if cos_def['entries'] == '':
        cos_def['entries'] = '1'

    cos_def['name'] = input('  Enter COS Definition name [cos_def]: ')
    if cos_def['name'] == '':
        cos_def['name'] = 'cos_def'

    cos_def['parent'] = input('  Enter definition parent DN [' + cos_template['suffix'] + ']: ')
    if cos_def['parent'] == '':
        cos_def['parent'] = cos_template['suffix']

    answer = input('  Create definition parent entry [n]: ')
    if answer == 'y':
        cos_def['create_parent'] = True
        answer = input('  Add default ACI\'s to parent entry [y]: ')
        if answer == '' or answer == 'y':
            cos_def['skip_aci'] = False

    if cos_type == 'classic':
        cos_def['cosSpecifier'] = input('  Enter COS specifier [description]: ')
        if cos_def['cosSpecifier'] == '':
            cos_def['cosSpecifier'] = 'description'

    if cos_type == 'indirect':
        cos_def['indirectSpecifier'] = input('  Enter COS indirect specifier [description]: ')
        if cos_def['indirectSpecifier'] == '':
            cos_def['indirectSpecifier'] = 'description'

    print ('  Enter COS attributes, press Enter when finished.')
    while True:
        value = input('  COS attribute: ')
        if value == '':
            break
        cos_def['attr_list'].append(value)

    print ('\n')
    write_cos(None, cos_type, cos_template, cos_def)


#
# Write the Mods to the LDIF
#
def write_mods(LDIF, entry):
    if LDIF is None:
        LDIF = open_ldif(None)

    if entry['mixops']:
        added_sup = 0
        if entry['mix-random']:
            operations = ['add', 'mod', 'modrdn', 'moddn', 'delete']
            addc = int(entry['mix-add'])
            delc = int(entry['mix-del'])
            modc = int(entry['mix-mod'])
            mdnc = int(entry['mix-moddn'])
            mrdnc = int(entry['mix-modrdn'])
            entry['entries'] = addc
            total_ops = addc + delc + modc + mdnc + mrdnc

            while total_ops:
                op = random_pick(operations)
                if op == 'add':
                    if addc < 1:
                        # no more adds to do
                        operations.remove('add')
                        continue

                    LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(addc, entry['mix-add']), entry['parent']))
                    LDIF.write("changetype: add\n")
                    LDIF.write("objectclass: top\n")
                    LDIF.write("objectclass: person\n")
                    LDIF.write("objectclass: inetorgperson\n")
                    LDIF.write("uid: %s%s\n" % (entry['name'], get_index(addc, entry['mix-add'])))
                    LDIF.write("sn: %s\n" % get_index(addc, entry['mix-add']))
                    LDIF.write("givenname: %s\n" % entry['name'])
                    LDIF.write("cn: %s %s\n" % (entry['name'], get_index(addc, entry['mix-add'])))
                    #LDIF.write("userpassword: %s%s\n" % (entry['name'], get_index(addc, entry['mix-add'])))
                    LDIF.write("\n")
                    addc -= 1
                    total_ops -= 1
                    continue

                if op == 'mod':
                    if modc < 1:
                        # no more mods to do
                        operations.remove('mod')
                        continue

                    LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(modc, entry['mix-mod']), entry['parent']))
                    LDIF.write("changetype: modify\n")
                    LDIF.write("replace: description\n")
                    LDIF.write("description: my new new description\n")
                    LDIF.write("\n")
                    modc -= 1
                    total_ops -= 1
                    continue

                if op == 'delete':
                    if delc < 1:
                        # no more deletes to do
                        operations.remove('delete')
                        continue

                    LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(delc, entry['mix-del']), entry['parent']))
                    LDIF.write("changetype: delete\n")
                    LDIF.write(" \n")
                    delc -= 1
                    total_ops -= 1
                    continue

                if op == 'modrdn':
                    if mrdnc < 1:
                        # no more modrdns to do
                        operations.remove('modrdn')
                        continue

                    LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(mrdnc, entry['mix-modrdn']),
                                    entry['parent']))
                    LDIF.write("changetype: modrdn\n")
                    LDIF.write("newrdn: cn=%s%s\n" % (entry['name'], get_index(mrdnc, entry['mix-modrdn'])))
                    LDIF.write("deleteoldrdn: 1\n")
                    LDIF.write("\n")
                    mrdnc -= 1
                    total_ops -= 1
                    continue

                if op == 'moddn':
                    if mdnc < 1:
                        # no more moddns to do
                        operations.remove('moddn')
                        continue

                    if not added_sup:
                        LDIF.write("dn: ou=New Branch,%s\n" % (entry['parent']))
                        LDIF.write("changetype: add\n")
                        LDIF.write("objectclass: top\n")
                        LDIF.write("objectclass: organizationalunit\n")
                        LDIF.write("ou: New Branch\n\n")
                        added_sup = 1

                    LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(mdnc, entry['mix-moddn']),
                                    entry['parent']))
                    LDIF.write("changetype: modrdn\n")
                    LDIF.write("newrdn: cn=%s%s\n" % (entry['name'], get_index(mdnc, entry['mix-moddn'])))
                    LDIF.write("deleteoldrdn: 1\n")
                    LDIF.write("newsuperior: ou=New Branch,%s\n" % entry['parent'])
                    LDIF.write("\n")
                    entry['mod_op'] = 'modrdn'  # for delete entries as the end
                    entry['newsuperior'] = "ou=New Branch,%s" % entry['parent']
                    mdnc -= 1
                    total_ops -= 1
                    continue

                if op == '':
                    break

        else:
            # Sequentialy do the adds, mods, modrns, and deletes
            entry['entries'] = entry['mix-add']
            added_sup = 0
            idx = 1

            while idx <= int(entry['mix-add']):
                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-add']), entry['parent']))
                LDIF.write("changetype: add\n")
                LDIF.write("objectclass: top\n")
                LDIF.write("objectclass: person\n")
                LDIF.write("objectclass: inetorgperson\n")
                LDIF.write("uid: %s%s\n" % (entry['name'], get_index(idx, entry['mix-add'])))
                LDIF.write("sn: %s\n" % get_index(idx, entry['mix-add']))
                LDIF.write("givenname: %s\n" % entry['name'])
                LDIF.write("cn: %s %s\n" % (entry['name'], get_index(idx, entry['mix-add'])))
                #LDIF.write("userpassword: %s%s\n" % (entry['name'], get_index(idx, entry['mix-add'])))
                LDIF.write("\n")
                idx += 1

            idx = 1
            while idx <= int(entry['mix-mod']):
                # Do mod: add, replace, delete
                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-mod']), entry['parent']))
                LDIF.write("changetype: modify\n")
                LDIF.write("replace: description\n")
                LDIF.write("description: my new new description\n")
                LDIF.write("\n")

                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-mod']), entry['parent']))
                LDIF.write("changetype: modify\n")
                LDIF.write("add: sn\n")
                LDIF.write("sn: my new surname\n")
                LDIF.write("\n")

                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-mod']), entry['parent']))
                LDIF.write("changetype: modify\n")
                LDIF.write("delete: description\n")
                LDIF.write("\n")

                # multiple mod op: sn, userpassword, description
                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-mod']), entry['parent']))
                LDIF.write("changetype: modify\n")
                LDIF.write("replace: sn\n")
                LDIF.write("sn: my new new surname\n")
                LDIF.write("-\n")
                LDIF.write("replace: userpassword\n")
                LDIF.write("userpassword: newpassword%s\n" % get_index(idx, entry['mix-mod']))
                LDIF.write("-\n")
                LDIF.write("replace: description\n")
                LDIF.write("description: multi mod operation\n")
                LDIF.write("\n")

                idx += 1

            idx = 1
            while idx <= int(entry['mix-modrdn']):
                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-modrdn']), entry['parent']))
                LDIF.write("changetype: modrdn\n")
                LDIF.write("newrdn: cn=%s%s\n" % (entry['name'], get_index(idx, entry['mix-modrdn'])))
                LDIF.write("deleteoldrdn: 1\n")
                LDIF.write("\n")
                entry['mod_op'] = 'modrdn'  # for delete entries as the end
                idx += 1

            idx = 1
            while idx <= int(entry['mix-moddn']):  # newsuperior
                if not added_sup:
                    LDIF.write("dn: ou=New Branch,%s\n" % (entry['parent']))
                    LDIF.write("changetype: add\n")
                    LDIF.write("objectclass: top\n")
                    LDIF.write("objectclass: organizationalunit\n")
                    LDIF.write("ou: NeW Branch\n\n")
                    added_sup = 1

                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-moddn']), entry['parent']))
                LDIF.write("changetype: modrdn\n")
                LDIF.write("newrdn: cn=%s%s\n" % (entry['name'], get_index(idx, entry['mix-moddn'])))
                LDIF.write("deleteoldrdn: 1\n")
                LDIF.write("newsuperior: ou=New Branch,%s\n" % entry['parent'])
                LDIF.write("\n")
                entry['mod_op'] = 'modrdn'  # for delete entries as the end
                entry['newsuperior'] = "ou=New Branch,%s" % entry['parent']
                idx += 1

            idx = 1
            while idx <= int(entry['mix-del']):
                LDIF.write("dn: uid=%s%s,%s\n" % (entry['name'], get_index(idx, entry['mix-del']), entry['parent']))
                LDIF.write("changetype: delete\n")
                LDIF.write(" \n")
                idx += 1

    else:
        if entry['create_entries']:
            write_users(LDIF, entry, True)

        if entry['modify_entries']:
            idx = 1
            random_val = False
            if entry['attr_val'] == 'RANDOM':
                entry['attr_val'] = get_random_value('alpha')
                random_val = True
            while idx <= int(entry['entries']):
                dn = ("dn: %s=%s%s,%s\n" % (entry['rdn'], entry['name'], get_index(idx, entry['entries']),
                         entry['parent']))
                mod_count = 0
                while mod_count < int(entry['mod_num']):
                    LDIF.write(dn)
                    if entry['mod_op'] == 'modrdn':
                        LDIF.write('changetype: modrdn\n')
                        LDIF.write('newrdn: %s%s\n' % (entry['newrdn'], get_index(idx, entry['entries'])))
                        LDIF.write('deleteoldrdn: %s\n' % (entry['deleteoldrdn']))
                        if entry['newsuperior']:
                            LDIF.write('newsuperior: %s\n' % (entry['newsuperior']))
                    else:
                        LDIF.write('changetype: modify\n')
                        LDIF.write('%s: %s\n' % (entry['mod_op'], entry['mod_attr']))
                        if entry['attr_val'] != '':
                            if random_val:
                                entry['attr_val'] = get_random_value('alpha')
                            if entry['mod_op'] == 'add':
                                # Add the index number to the value, so we don't get "type or value exists"
                                LDIF.write('%s: %s%d\n' % (entry['mod_attr'], entry['attr_val'], mod_count))
                            else:
                                LDIF.write('%s: %s\n' % (entry['mod_attr'], entry['attr_val']))
                    LDIF.write('\n')
                    mod_count += 1
                idx += 1
        if entry['add_to_group']:
            group_dn = ("dn: %s\n" % entry['group'])
            LDIF.write(group_dn)
            LDIF.write('changetype: modify\n')
            mod_count = 1
            while mod_count <= int(entry['entries']):
                LDIF.write('add: uniquemember\n')
                LDIF.write('uniquemember: uid=%s%s,%s\n' % (entry['name'],
                           get_index(mod_count, entry['entries']), entry['parent']))
                LDIF.write('-\n')
                mod_count += 1
            LDIF.write('\n')

    if entry['delete_entries']:
        idx = 1
        while idx <= int(entry['entries']):
            if entry['mod_op'] == 'modrdn':
                # We have to delete the entry by its new RDN
                if entry['newsuperior']:
                    if entry['mixops']:
                        dn = 'dn: cn=%s%s,%s\n' % (entry['name'], get_index(idx, entry['entries']), entry['newsuperior'])
                    else:
                        dn = 'dn: %s%s,%s\n' % (entry['newrdn'], get_index(idx, entry['entries']), entry['newsuperior'])
                else:
                    if entry['mixops']:
                        dn = 'dn: cn=%s%s,%s\n' % (entry['name'], get_index(idx, entry['entries']), entry['parent'])
                    else:
                        dn = 'dn: %s%s,%s\n' % (entry['newrdn'], get_index(idx, entry['entries']), entry['parent'])
            else:
                dn = ("dn: %s=%s%s,%s\n" % (entry['rdn'], entry['name'], get_index(idx, entry['entries']),
                          entry['parent']))
            LDIF.write(dn)
            LDIF.write('changetype: delete\n')
            LDIF.write('\n')
            idx += 1

    LDIF.close()
    print ('Done.')


#
# Interactive Mod Creation
#
def create_mods():
    entry = {
        'schema': [],
        'skip_aci': True,
        'create_parent': False,
        'modify_entries': False,
        'create_entries': False,
        'delete_entries': False,
        'unnorm': False,
        'createorgchart': False,
        'size': -1,
        'add_to_group': False,
        'mix-moddn': '0',
        'mix-modrdn': '0',
        'mod_op': '',
        'newsuperior': ''
    }

    print ('\nCreate Modification LDIF')

    entry['name'] = input('  Enter entry name [test_entry]: ')
    if entry['name'] == '':
        entry['name'] = 'test_entry'

    entry['rdn'] = input('  Enter rdn attribute [uid]: ')
    if entry['rdn'] == '':
        entry['rdn'] = 'uid'

    entry['suffix'] = input('  Enter base suffix DN [dc=example,dc=com]: ')
    if entry['suffix'] == '':
        entry['suffix'] = 'dc=example,dc=com'

    entry['parent'] = input('  Enter entry parent DN [' + entry['suffix'] + ']: ')
    if entry['parent'] == '':
        entry['parent'] = entry['suffix']

    answer = input('  Create parent entry [n]: ')
    if answer == 'y':
        entry['create_parent'] = True
        answer = input('  Add default ACI\'s to parent entry [y]: ')
        if answer == '' or answer == 'y':
            entry['skip_aci'] = False

    #
    # Mixed operations
    #
    entry['mixops'] = input('  Do all operations (add, mod, delete, and modrdn) [n]: ')
    if entry['mixops'] == 'y':
        entry['mix-add'] = input('    Number of add\'s [1000]: ')
        if entry['mix-add'] == '':
            entry['mix-add'] = '1000'

        entry['mix-mod'] = input('    Number of modify\'s [1000]: ')
        if entry['mix-mod'] == '':
            entry['mix-mod'] = '1000'

        entry['mix-moddn'] = input('    Number of mod-dn\'s (change entire dn) [0]: ')
        if entry['mix-moddn'] == '':
            entry['mix-moddn'] = '0'

        if entry['mix-moddn'] == '0':
            entry['mix-modrdn'] = input('    Number of mod-rdn\'s (change only the rdn) [0]: ')
            if entry['mix-modrdn'] == '':
                entry['mix-modrdn'] = '0'

        entry['mix-del'] = input('    Number of delete\'s [0]: ')
        if entry['mix-del'] == '':
            entry['mix-del'] = '0'

        entry['mix-random'] = input('    Randomize operations (Warning: not all operations might succeed) [n]: ')
        if entry['mix-random'] == 'y':
            entry['mix-random'] = True
        else:
            entry['mix-random'] = False

    else:
        entry['mixops'] = False

        #
        # Gather specific details about the modifications
        #
        entry['entries'] = 'invalid'
        while not entry['entries'].isdigit():
            entry['entries'] = input('  Enter number of entries [500]: ')
            if entry['entries'] == '':
                entry['entries'] = '500'

        answer = input('  Create entries [y]: ')
        if answer == 'y' or answer == '':
            entry['create_entries'] = True
            entry['passwd'] = input('    Enter userpassword value (default is the user\'s "uid" value): ')

            answer = input('    Use unnormalized DN\'s [n]: ')
            if answer == 'y':
                entry['unnorm'] = True

            custom_schema = input('    Add additional attributes [n]: ')
            if custom_schema == 'y':
                print ('      Enter \"attribute: value\", press Enter when finished.')
                while True:
                    value_pair = input('      Attr/Value: ')
                    if value_pair == '':
                        break
                    entry['schema'].append(value_pair)

            while not entry['size'].isdigit():
                entry['size'] = input('    Enter entry size(in bytes) or press ENTER for default size: ')
                if entry['size'] == '':
                    entry['size'] = 0
                    break

        answer = input('  Modify entries [n]: ')
        if answer == 'y':
            entry['modify_entries'] = True
            entry['mod_op'] = 'invalid'
            while (entry['mod_op'] != 'add' and entry['mod_op'] != 'delete'
                        and entry['mod_op'] != 'replace' and entry['mod_op'] != 'modrdn'):
                entry['mod_op'] = input('    Changetype operation (add, replace, delete, modrdn) [replace]: ')
                if entry['mod_op'] == '':
                    entry['mod_op'] = 'replace'

            if entry['mod_op'] == 'modrdn':
                    entry['mod_num'] = '1'
                    entry['newrdn'] = ''

                    while entry['newrdn'] == '':
                        entry['newrdn'] = input('    New rdn: ')
                    entry['deleteoldrdn'] = input('    Delete old rdn [y]: ')
                    if entry['deleteoldrdn'] == '' or entry['deleteoldrdn'] == 'y':
                        entry['deleteoldrdn'] = '1'
                    else:
                        entry['deleteoldrdn'] = '0'
                    entry['newsuperior'] = input('    New superior DN [press enter to skip]: ')
                    if entry['newsuperior'] == '':
                        entry['newsuperior'] = False
            else:
                entry['mod_attr'] = input('    Enter attribute to modify [description]: ')
                if entry['mod_attr'] == '':
                    entry['mod_attr'] = 'description'

                entry['attr_val'] = input('    Enter attribute value: ')

                entry['mod_num'] = 'invalid'
                while not entry['mod_num'].isdigit():
                    if entry['mod_op'] == 'modrdn':
                        entry['mod_num'] = '1'

                    entry['mod_num'] = input('    Enter number of times to perform mod [1]: ')
                    if entry['mod_num'] == '':
                        entry['mod_num'] = '1'
        else:
            answer = input('  Add entries to a group [n]: ')
            if answer == 'y':
                entry['group'] = ''
                while entry['group'] == '':
                    entry['group'] = input('    Enter group name: ')
                entry['add_to_group'] = True

            else:
                entry['mod_op'] = ''

    #
    # Delete/cleanup/purge the entries
    #
    answer = input('  Delete entries [n]: ')
    if answer == 'y':
        entry['delete_entries'] = True

    write_mods(None, entry)
    return


def value_yes(value):
    val = value.lower()
    if val == 'y' or val == 'yes':
        return True
    else:
        return False


def verify_yes_no(param, value):
    val = value.lower()
    if val != 'y' and val != 'yes' and val != 'n' and val != 'no':
        print ('Invalid value for yes/no parameter: %s' % param)
        exit(1)


def parse_inf_file(inf_file):
    directive = 'none'
    gen = {}
    users = {}
    groups = {}
    roles = {}
    cos = {}
    mods = {}
    params = []

    try:
        inf = open(inf_file, "r")
        params = list(inf)
        inf.close()
    except IOError:
        print ('Failed to open file ' + inf_file)
        exit(1)

    for p in params:
        if p.lower() == '[general]':
            directive = 'gen'
            continue
        elif p.lower() == '[users]':
            directive = 'users'
            continue
        elif p.lower() == '[groups]':
            directive = 'groups'
            continue
        elif p.lower() == '[roles]':
            directive = 'roles'
            continue
        elif p.lower() == '[cos]':
            directive = 'cos'
            continue
        elif p.lower() == '[mods]':
            directive = 'mods'
            continue
        elif p == '':
            directive = 'none'
            continue

        # MARK TODO - Add IPA user/host

        val = p.split('=', 1)[1].lstrip()

        if directive == 'gen':
            gen = {}
            if p.lower().startswith('outputfile'):
                gen['outfile'] = val
            if p.lower().startswith('backendsuffix'):
                gen['backendsuffix'] = val
            if p.lower().startswith('parentsuffix'):
                gen['parentsuffix'] = val
            if p.lower().startswith('createaparent'):
                verify_yes_no(p, val)
                gen['createparent'] = val
            if p.lower().startswith('defaultacis'):
                verify_yes_no(p, val)
                if value_yes(val):
                    gen['skip_aci'] = val
            if p.lower().startswith('createorgchart'):
                gen['createorgchart'] = val

        if directive == 'users':
            if p.lower().startswith('rdnattr'):
                users['rdnattr'] = val
            if p.lower().startswith('rdnval'):
                users['rdnval'] = val
            if p.lower().startswith('numentries'):
                users['numentries'] = val
            if p.lower().startswith('padding'):
                verify_yes_no(p, val)
                users['padding'] = val
            if p.lower().startswith('template'):
                users['template'] = val
            if p.lower().startswith('attr_value'):
                users['attr_value'] = val
            if p.lower().startswith('normalizeddn'):
                verify_yes_no(p, val)
                users['normalizeddn'] = val
            if p.lower().startswith('password'):
                users['password'] = val
            if p.lower().startswith('entrysize'):
                users['entrysize'] = val

        if directive == 'groups':
            if p.lower().startswith('numgroups'):
                groups['numgroups'] = val
            if p.lower().startswith('rdnval'):
                groups['rdnval'] = val
            if p.lower().startswith('numentries'):
                groups['numentries'] = val
            if p.lower().startswith('padding'):
                verify_yes_no(p, val)
                groups['padding'] = val
            if p.lower().startswith('template'):
                groups['template'] = val
            if p.lower().startswith('attr_value'):
                groups['attr_value'] = val
            if p.lower().startswith('membershipattr'):
                groups['membershipattr'] = val
            if p.lower().startswith('createmembers'):
                verify_yes_no(p, val)
                groups['createmembers'] = val
            if p.lower().startswith('createuniquemembers'):
                verify_yes_no(p, val)
                groups['createuniquemembers'] = val
            # member settings
            if p.lower().startswith('membertemplate'):
                groups['membertemplate'] = val
            if p.lower().startswith('memberrdnattr'):
                groups['memberrdnattr'] = val
            if p.lower().startswith('memberrdnattr'):
                groups['memberrdnattr'] = val
            if p.lower().startswith('memberparent'):
                groups['memberparent'] = val
            if p.lower().startswith('memberpassword'):
                groups['memberpassword'] = val
            if p.lower().startswith('memberattr_value'):
                groups['memberattr_value'] = val
            if p.lower().startswith('membersize'):
                groups['membersize'] = val

        if directive == 'roles':
            if p.lower().startswith('numroles'):
                roles['numroles'] = val
            if p.lower().startswith('roletype'):
                roles['roletype'] = val
            if p.lower().startswith('rolefilter'):
                roles['rolefilter'] = val

        if directive == 'cos':
            if p.lower().startswith('cos_type'):
                cos['cos_type'] = val
            # templates
            if p.lower().startswith('cos_templatename'):
                cos['cos_templatename'] = val
            if p.lower().startswith('cos_templatenum'):
                cos['cos_templatenum'] = val
            if p.lower().startswith('cos_templateparent'):
                cos['cos_templateparent'] = val
            if p.lower().startswith('cos_templatecreateparent'):
                cos['cos_templatecreateparent'] = val
            if p.lower().startswith('cos_templateattr'):
                cos['cos_templateattr'] = val
            if p.lower().startswith('cos_templatepriority'):
                cos['cos_templatepriority'] = val
            # definitions
            if p.lower().startswith('cos_defname'):
                cos['cos_defname'] = val
            if p.lower().startswith('cos_defparent'):
                cos['cos_defparent'] = val
            if p.lower().startswith('cos_defcreateparent'):
                cos['cos_defcreateparent'] = val
            if p.lower().startswith('cos_defnum'):
                cos['cos_defnum'] = val
            if p.lower().startswith('cosattr'):
                cos['cosattr'] = val
            if p.lower().startswith('cosspecifier'):
                cos['cosspecifier'] = val
            if p.lower().startswith('cosindirectspecifier'):
                cos['cosindirectspecifier'] = val

        if directive == 'mods':
            if p.lower().startswith('template'):
                mods['template'] = val
            # mixed mods
            if p.lower().startswith('mixops'):
                verify_yes_no(p, val)
                mods['mixops'] = val
            if p.lower().startswith('mixadds'):
                mods['mix-adds'] = val
            if p.lower().startswith('mixmods'):
                mods['mix-mods'] = val
            if p.lower().startswith('mixmoddns'):
                mods['mix-moddns'] = val
            if p.lower().startswith('mixmodrdns'):
                mods['mix-modrdns'] = val
            if p.lower().startswith('mixdels'):
                mods['mix-dels'] = val
            if p.lower().startswith('mixrandom'):
                mods['mix-random'] = val
            # specific mods
            if p.lower().startswith('createentries'):
                verify_yes_no(p, val)
                mods['createentries'] = val
            if p.lower().startswith('attr_value'):
                mods['attr_value'] = val
            if p.lower().startswith('modop'):
                mods['modop'] = val
            if p.lower().startswith('modval'):
                mods['modval'] = val
            if p.lower().startswith('modcount'):
                mods['modcount'] = val

    if not gen:
        print ('Missing required directive [General]')
        exit(1)

    if users:
        users.update(gen)

    if groups:
        groups.update(gen)

    if roles:
        roles.update(gen)

    if cos:
        cos.update(gen)

    if mods:
        mods.update(gen)


#
# This formatter is for help section of option parsing so newlines are not stripped
#
class IndentedHelpFormatterWithNL(IndentedHelpFormatter):
    def format_description(self, description):
        if not description:
            return ""
        desc_width = self.width - self.current_indent
        indent = " " * self.current_indent
        # the above is still the same
        bits = description.split('\n')
        formatted_bits = [
            textwrap.fill(bit,
            desc_width,
            initial_indent=indent,
            subsequent_indent=indent)
            for bit in bits]
        result = "\n".join(formatted_bits) + "\n"
        return result

    def format_option(self, option):
        result = []
        opts = self.option_strings[option]
        opt_width = self.help_position - self.current_indent - 2
        if len(opts) > opt_width:
            opts = "%*s%s\n" % (self.current_indent, "", opts)
            indent_first = self.help_position
        else:
            # start help on same line as opts
            opts = "%*s%-*s  " % (self.current_indent, "", opt_width, opts)
            indent_first = 0
        result.append(opts)
        if option.help:
            help_text = self.expand_default(option)
            # Everything is the same up through here
            help_lines = []
            for para in help_text.split("\n"):
                help_lines.extend(textwrap.wrap(para, self.help_width))
            # Everything is the same after here
            result.append("%*s%s\n" % (indent_first, "", help_lines[0]))
            result.extend(["%*s%s\n" % (self.help_position, "", line)
            for line in help_lines[1:]])
        elif opts[-1] != "\n":
            result.append("\n")
        return "".join(result)


#
# handle control-C cleanly
#
def signal_handler(signal, frame):
    print ('')
    exit(0)


#
#
# This was run in either command line mode or interactive
#
#
def main():
    global verbose
    global firstnames
    global lastnames
    global orgUnits
    global orgManagers
    global exec_presidents
    global presidents
    global vice_presidents
    global directors
    global localities
    global titles
    global padding

    # setup the control-C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    #
    # Read in the name files
    #
    try:
        FIRSTNAMES = open(DataDir + 'dbgen-GivenNames', 'r')
        firstnames = list(FIRSTNAMES)
        FIRSTNAMES.close()
    except IOError:
        if verbose:
            print ('Can\'t open file: ' + DataDir + 'dbgen-GivenNames')
            print ('Using internal first name list')

    try:
        LASTNAMES = open(DataDir + 'dbgen-FamilyNames', 'r')
        lastnames = list(LASTNAMES)
        LASTNAMES.close()
    except IOError:
        if verbose:
            print ('Can\'t open file: ' + DataDir + 'dbgen-GivenNames')
            print ('Using internal last name list')

    #########################################################
    # Command line mode
    #########################################################
    if len(sys.argv) > 1:
        action_obj = {
            'schema': [],
            'member_schema': []
        }

        desc = ("""LDIF file generation tool (v""" + VERSION + """).  This script""" +
                     """ can be used to create a variety of custom LDIF files: from """ +
                     """user entries, organizational units, groups, COS defintions/""" +
                     """templates, and role entries.  Also a customizable modification """ +
                     """LDIF can be created that can be run by ldapmodify.  There are """ +
                     """a few special KEYWORDS that be used to generate/specify special """ +
                     """values(RANDOM, RANDOM_PICK, and SEQ_SET.  When RANDOM is used, a """ +
                     """random string of characters replaces that keyword. RANDOM_PICK """ +
                     """randomly selects a value from a semicolon separated list:  """ +
                     """\"RANDOM_PICK: orange; apple; grapes\".  SEQ_SET uses the next """ +
                     """value in the list after each call, and then will continue to loop """ +
                     """over these values sequentially: \"SEQ_SET: one; two; three\" - """ +
                     """this is useful to evenly spread out values.""")

        parser = optparse.OptionParser(description=desc, formatter=IndentedHelpFormatterWithNL())

        # General options
        parser.add_option('-V', '--version', help='Display version of tool.', action='store_true',
                                        default=False, dest='version')
        parser.add_option('-v', '--verbose', help='Verbose output.', action='store_true', default=False, dest='verbose')
        parser.add_option('-o', '--outfile', help='The LDIF output file, (default "/tmp/out.ldif")', dest='file',
                                      default='/tmp/out.ldif')
        parser.add_option('-a', '--action', help='Actions: create-user, create-ipa-user, create-ipa-host, create-group, create-ou, ' +
                                      'create-role, create-cos, or create-mod (default "create-user")',
                                      dest='action', default='create-user')
        parser.add_option('-e', '--entryname', help='The name of the entry (omit this option to use "real names")',
                                      dest='name', default='')
        parser.add_option('-s', '--base-suffix', help='The base suffix/backend (default is "dc=example,dc=com")',
                                      dest='suffix', default='dc=example,dc=com')
        parser.add_option('-p', '--parent', help='The parent DN of the entry (default is the base suffix)',
                                      dest='parent', default='')
        parser.add_option('-c', '--create-parent', help='Create the parent entry', action="store_true",
                                      default=False, dest='createParent')
        parser.add_option('-r', '--rdn', help='The rdn attribute of the entry (default is "cn")',
                                      dest='rdn', default='cn')
        parser.add_option('-n', '--numentries', help='The number of entries to create (default 1)',
                                      dest='numEntries', default='1')
        parser.add_option('-f', '--template', help='Template file for entry creation', dest='template',
                                      default='')
        parser.add_option('-t', '--attr', help='An "attribute: value" pair to add to the entry.  ' +
                                      'RANDOM, RANDOM_PICK, and SEQ_SET are allowed', action="append", dest='schema')
        parser.add_option('-w', '--passwd', help='The password to use for user entries (default is the ' +
                                      'user\'s "uid" value)', dest='passwd', default='')
        parser.add_option('-b', '--no-aci', help='Do not add any default aci\'s', dest='skip_aci', action="store_true",
                                       default=False)
        parser.add_option('-u', '--unnormal-dn', help='Uses unnormalized DN\'s', dest='unnormal', action="store_true",
                                       default=False)
        parser.add_option('-d', '--nopad', help='Do not add any leading zero\'s to entry index(LDIF will ' +
                                      'not work with the client tool "ldclt"', dest='nopadding', action="store_true",
                                       default=False)
        parser.add_option('-l', '--entrysize', help='Entry size (in bytes)', dest='entrysize', default='0')
        parser.add_option('-m', '--createorgchart', help='Create organization entries', dest='createorgchart',
                                      action="store_true", default=False)

        # Handle the every growing list of options for each action
        parser.add_option('-g', '--memberopt',
            help='template=<template file for member entries>\n' +
                 'members=<number of members>\n' +
                 'memberattr=<membership attribute>\n' +
                 'createmembers\n' +
                 'createuniquemembers\n' +
                 'name=<member\'s rdn attribute value>\n' +
                 'parent=<the member entry\'s parent DN>\n' +
                 'createparent\n' +
                 'rdn=<rdn attribute for member\n' +
                 'passwd=<member\s password, skip to use uid>\n' +
                 'attr=<"attribute: value" pair>\n',
            action="append", dest='memberopts')
        parser.add_option('-i', '--roleopt',
            help='roletype=<managed, filtered, or nested>\n' +
                 'rolefilter=<search filter for filtered role>\n' +
                 'nestedrole=<DN of nested role>\n',
            action="append", dest='roleopts')
        parser.add_option('-j', '--cosopts',
            help='cos_type=<classic, pointer, or indirect> \n' +
                 'cos_templatename=<name of COS template>\n' +
                 'cos_templatenum=<number of COS templates to create>\n' +
                 'cos_templateparent=<DN of template\'s parent entry>\n' +
                 'cos_templatecreateparent\n' +
                 'cos_templateattr=<COS template "attribute: value" pair>\n' +
                 'cos_templatepriority=<COS template priority>\n' +
                 'cos_defname=<COS definition name>\n' +
                 'cos_defnum=<number of COS defintions>\n' +
                 'cos_defparent=<DN of COS definition\'s parent entry>\n' +
                 'cos_defcreateparent\n' +
                 'cosattr=<COS attribute>\n' +
                 'cosspecifier=<COS specifier>\n' +
                 'cosindirectspecifier=<COS indirect specifier>\n',
            action="append", dest='cosopts')
        parser.add_option('-k', '--modopts',
            help='modcreateentry\n' +
                 'modop=<modify operation: add, replace, delete>\n' +
                 'modattr=<attribute to modify>\n' +
                 'modvalue=<attribute value for the mod>\n' +
                 'modcount=<number of times to perform the mod> \n' +
                 'moddeleteentry\n',
             action="append", dest='modopts')

        #
        # Process the options
        #
        (args, opts) = parser.parse_args()

        if len(sys.argv) == 2 and args.verbose:
            verbose = True
        else:
            if args.version:
                print ('LDIF generator (v' + VERSION + ')\n')
                exit(0)

            # general options
            action_obj['create_parent'] = args.createParent
            action_obj['createorgchart'] = args.createorgchart
            if not action_obj['create_parent'] and action_obj['createorgchart']:
                action_obj['create_parent'] = True
            action_obj['file'] = args.file
            if args.template != '':
                action_obj['template_file'] = args.template
                read_template(action_obj, 0)
            verbose = args.verbose
            if args.schema:
                action_obj['schema'] = args.schema
            action_obj['name'] = args.name
            action_obj['entries'] = args.numEntries
            action_obj['suffix'] = args.suffix
            if args.parent == '':
                action_obj['parent'] = args.suffix
            else:
                action_obj['parent'] = args.parent
            action_obj['rdn'] = args.rdn
            action_obj['passwd'] = args.passwd
            action_obj['skip_aci'] = args.skip_aci
            action_obj['unnorm'] = args.unnormal
            if args.entrysize.isdigit():
                action_obj['size'] = int(args.entrysize)
            else:
                action_obj['size'] = 0
                if verbose:
                    print ('Size (%s) is not a number, ignoring value...' % args.entrysize)
            if args.nopadding:
                padding = False

            LDIF = open_ldif(args.file)

            #
            # Create Users
            #
            if args.action == 'create-user':
                write_users(LDIF, action_obj)
                print ('Done.')

            #
            # Create Organizational Units
            #
            elif args.action == 'create-ou':
                write_ou(LDIF, action_obj)

            #
            # Create Groups
            #
            elif args.action == 'create-group':
                action_obj['member_parent'] = args.parent
                action_obj['create_members'] = False
                action_obj['create_unique_members'] = False
                action_obj['create_member_parent'] = False

                for groupOpt in args.memberopts:
                    parts = groupOpt.split('=')
                    keyword = parts[0].lower().rstrip()
                    value = parts[1]
                    if keyword == 'template':
                        action_obj['member_template_file'] = value
                    elif keyword == 'members':
                        action_obj['members'] = value
                    elif keyword == 'memberattr':
                        action_obj['member_attr'] = value
                    elif keyword == 'createmembers':
                        action_obj['create_members'] = True
                    elif keyword == 'createuniquemembers':
                        action_obj['create_unique_members'] = True
                    elif keyword == 'name':
                        action_obj['member_name'] = value
                    elif keyword == 'parent':
                        action_obj['member_parent'] = value
                    elif keyword == 'createparent':
                        action_obj['create_member_parent'] = True
                    elif keyword == 'passwd':
                        action_obj['member_passwd'] = args.password
                    elif keyword == 'rdn':
                        action_obj['member_rdn'] = value
                    elif keyword == 'attr':
                        action_obj['member_schema'].append(value)
                write_group(LDIF, action_obj)

            #
            # Create Roles
            #
            elif args.action == 'create-role':
                action_obj['role_type'] = 'managed'
                action_obj['role_list'] = []

                for roleOpt in args.roleopts:
                    parts = roleOpt.split('=')
                    keyword = parts[0].lower().rstrip()
                    value = parts[1].lstrip()
                    if keyword == 'rolefilter':
                        action_obj['filter'] = value
                    elif keyword == 'nestedrole':
                        action_obj['role_list'].append(value)
                    elif keyword == 'roletype':
                        action_obj['role_type'] = value
                write_role(LDIF, action_obj)

            #
            # Create COS
            #
            elif args.action == 'create-cos':
                cos_type = 'classic'
                cos_def = {
                    'entries': '1',
                    'attr_list': [],
                    'create_parent': False,
                }
                cos_template = {
                    'entries': '0',
                    'create_parent': False
                }

                for cosOpt in args.cosopts:
                    parts = cosOpt.split('=')
                    keyword = parts[0].lower().rstrip()
                    value = parts[1].lstrip()
                    if keyword == 'cos_type':
                        cos_type = value
                    elif keyword == 'cos_templatename':
                        cos_template['name'] = value
                    elif keyword == 'cos_templatenum':
                        cos_template['entries'] = value
                    elif keyword == 'cos_templateparent':
                        cos_template['parent'] = value
                    elif keyword == 'cos_templatecreateparent':
                        cos_template['create_parent'] = True
                    elif keyword == 'cos_templateattr':
                        cos_template['attr_list'].append(value)
                    elif keyword == 'cos_templatepriority':
                        cos_template['priority'] = value
                    elif keyword == 'cos_defname':
                        cos_def['name'] = value
                    elif keyword == 'cos_defnum':
                        cos_def['entries'] = value
                    elif keyword == 'cos_defparent':
                        cos_def['parent'] = value
                    elif keyword == 'cos_defcreateparent':
                        cos_def['create_parent'] = True
                    elif keyword == 'cosattr':
                        cos_def['attr_list'].append(value)
                    elif keyword == 'cosspecifier':
                        cos_def['cosSpecifier'] = value
                    elif keyword == 'cosindirectspecifier':
                        cos_def['indirectSpecifier'] = value
                write_cos(LDIF, cos_type, cos_template, cos_def)

            #
            # Create Modification LDIF
            #
            elif args.action == 'create-mod':
                action_obj['create_entries'] = False
                action_obj['delete_entries'] = False

                for modOpt in args.modopts:
                    parts = modOpt.split('=')
                    keyword = parts[0].lower().rstrip()
                    value = parts[1].lstrip()
                    if keyword == 'modcreateentry':
                        action_obj['create_entries'] = True
                    elif keyword == 'modop':
                        action_obj['mod_op'] = value
                    elif keyword == 'modattr':
                        action_obj['mod_attr'] = value
                    elif keyword == 'modvalue':
                        action_obj['attr_val'] = value
                    elif keyword == 'modcount':
                        action_obj['mod_num'] = value
                    elif keyword == 'moddeleteentry':
                        action_obj['delete_entries'] = True
                action_obj['passwd'] = args.passwd
                write_mods(LDIF, action_obj)

            #
            # Typo?  Invalid action
            #
            else:
                print ('Invalid action: ' + args.action)

            LDIF.close()
            exit(0)

    ########################################################
    # Interactive mode
    ########################################################
    print ('LDIF Generator (v' + VERSION + ')')
    print ('')
    print ('1.  Create Users')
    print ('2.  Create IPA Users')
    print ('3.  Create IPA Hosts')
    print ('4.  Create Groups')
    print ('5.  Create Organizational Units')
    print ('6.  Create Managed Role')
    print ('7.  Create Filtered Role')
    print ('8.  Create Nested Role')
    print ('9.  Create Classic COS')
    print ('10.  Create Pointer COS')
    print ('11.  Create Indirect COS')
    print ('12. Create Modification LDIF')
    print ('13. Create Bad LDIF')
    print ('14. Create Nested LDIF')
    print ('')

    choice = input('Enter choice [1-12]: ')
    if choice == '':
        choice = '1'

    # Process the "decision"
    if choice == '1':
        create_users()
    elif choice == '2':
        create_ipa_users()
    elif choice == '3':
        create_ipa_hosts()
    elif choice == '4':
        create_group()
    elif choice == '5':
        create_ou()
    elif choice == '6':
        create_role('managed')
    elif choice == '7':
        create_role('filtered')
    elif choice == '8':
        create_role('nested')
    elif choice == '9':
        create_cos('classic')
    elif choice == '10':
        create_cos('pointer')
    elif choice == '11':
        create_cos('indirect')
    elif choice == '12':
        create_mods()
    elif choice == '13':
        create_bad_ldif()
    elif choice == '14':
        create_nested_ldif()

    else:
        print ('Invalid choice: ' + choice + ', exiting...')
        exit(1)
    return

if __name__ == '__main__':
    main()
