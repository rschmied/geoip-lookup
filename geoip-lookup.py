#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xchat
import GeoIP


__module_name__ = "geoip"
__module_version__ = "0.2"
__module_description__ = "Lookup location via GeoIP"
__module_author__ = "ralph.schmieder@gmail.com"


gi = GeoIP.open("/usr/share/GeoIP/GeoIPCity.dat", GeoIP.GEOIP_STANDARD)


def colordecode(word):
    # taken from: http://xchatdata.net/Scripting/TextFormatting"
    _B = re.compile('%B', re.IGNORECASE)  # bold
    _C = re.compile('%C', re.IGNORECASE)  # color (takes parameter)
    _R = re.compile('%R', re.IGNORECASE)  # reverse
    _O = re.compile('%O', re.IGNORECASE)  # original color
    _U = re.compile('%U', re.IGNORECASE)  # underline
    return _B.sub('\002', _C.sub('\003', _R.sub('\026', _O.sub('\017', _U.sub('\037', word)))))


def printLine(user, location):
    line = colordecode("%C8%B%s%O %U%s") % (user, location)
    xchat.emit_print("Generic Message", colordecode("%C8*%O"), line)


def printLocationLine(username, loc):
    record = gi.record_by_name(loc)
    if record is not None:
        user = "%s is from" % username
        items = list()
        for i in ['city', 'region_name', 'postal_code', 'country_name']:
            if record[i]:
                items.append(record[i])
        printLine(user, ", ".join(items))
    else:
        printLine(username, "Can't locate %s at %s" % (username, loc))


def getLocationWhoisNameCB(word, word_eol, userdata):
    printLocationLine(colordecode("%O%C2[%O" + word[0] + "%C2]%O"), word[2])
    return xchat.EAT_NONE


def getLocationCB(word, word_eol, userdata):
    all_users = not len(word) > 1
    channel = xchat.get_info("channel")
    if channel.startswith("#"):
        users = xchat.get_list('users')
        found = False or all_users
        for user in users:
            loc = user.host.split('@')[1]
            if not all_users and not xchat.nickcmp(user.nick, word[1]):
                found = True
            if found:
                printLocationLine(user.nick, loc)
            if found and not all_users:
                break
        if not found:
            xchat.emit_print(
                "Server Error", "Can't find user %s" % word[1])
    elif not all_users:
        xchat.command('whois %s' % word[1])
    else:
        xchat.emit_print("Generic Message", "@",
                         "no username given or not in a channel")
    return xchat.EAT_ALL


def getLocationJoinCB(word, word_eol, userdata):
    loc = word[2].split('@')[1]
    printLocationLine(word[0], loc)
    return xchat.EAT_NONE


def unloadCB(userdata):
    print colordecode("%C4Plugin %B" + __module_name__ + "%B " + __module_version__ + " unloaded.")


def setup():
    try:
        cmd = __module_name__.upper()
        xchat.hook_command(
            cmd, getLocationCB, help="""/{} [<userid>] Gets location of user(s).
            When used in a channel, list location for all users in the channel.
            Otherwise, print the location of the given user <userid>.""".format(cmd))
        xchat.hook_print("Join", getLocationJoinCB)
        xchat.hook_print("Whois Name Line", getLocationWhoisNameCB)
        xchat.hook_unload(unloadCB)
        print colordecode("%C4Plugin %B" + __module_name__ + "%B " + __module_version__ + " loaded.")

    except:
        print "can't hook callbacks to xchat"

if __name__ == '__main__':
    setup()
