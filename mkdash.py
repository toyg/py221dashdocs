# -*- coding: utf-8 -*-
__author__ = 'Giacomo Lacava'



import sqlite3
import os
from os.path import join, exists, dirname
from bs4 import BeautifulSoup as BS

PKGPATH = 'python221.docset/Contents/Resources'

DBPATH = join(PKGPATH, 'docSet.dsidx')

DOCPATH = join(PKGPATH, 'Documents')


def parsePage(pagePath, recordList):
    #print("parsing {}".format(pagePath))
    topDir = dirname(pagePath)
    with open(join(DOCPATH, pagePath), 'r', encoding='iso-8859-1') as pf:
        pageSoup = BS(pf)

    tts = [t for t in pageSoup.find_all('tt') if t.parent.name == 'a' and 'href' not in t.parent.attrs]
    for element in tts:
        elemType = "Type"
        if 'class' in element.attrs:
            elemType = element.attrs['class'][0].capitalize()
            if elemType == 'Member': elemType = 'Attribute'
        record = (element.text,
                  elemType,
                  '#'.join([pagePath, element.parent.attrs['name']]))
        recordList.append(record)

    childUL = pageSoup.find('ul', {'class': 'ChildLinks'})
    if childUL is not None:
        childAs = childUL.find_all('a')
        for a in childAs:
            parsePage(join(topDir, a.attrs['href']), recordList)

def parseModules(docPath):

    modIndex = join(docPath, 'modindex.html')
    soup = None
    records = []
    with open(modIndex, 'r', encoding='iso-8859-1') as mf:
        soup = BS(mf)

    tts = soup.find_all('tt')
    for tt in tts:
        module = tt.text
        path = tt.parent.attrs['href']
        #records.append((module, 'Module', path))
        parsePage(path, records)

    return records

def delete_dupes(cursor):
    mods = """AL
BaseHTTPServer
Bastion
CGIHTTPServer
Carbon.AE
Carbon.App
Carbon.CF
Carbon.Cm
Carbon.Ctl
Carbon.Dlg
Carbon.Evt
Carbon.Fm
Carbon.Help
Carbon.List
Carbon.Menu
Carbon.Mlte
Carbon.Qd
Carbon.Qdoffs
Carbon.Qt
Carbon.Res
Carbon.Scrap
Carbon.Snd
Carbon.TE
Carbon.Win
ColorPicker
ConfigParser
Cookie
DEVICE
EasyDialogs
FL
FrameWork
GL
HTMLParser
MacOS
MimeWriter
MiniAEFrame
PixMapWrapper
Queue
SUNAUDIODEV
ScrolledText
SimpleHTTPServer
SimpleXMLRPCServer
SocketServer
StringIO
TERMIOS
Tix
Tkinter
UserDict
UserList
UserString
W
__builtin__
__main__
_winreg
aepack
aetypes
aifc
al
anydbm
applesingle
array
asyncore
atexit
audioop
base64
binascii
binhex
bisect
bsddb
buildtools
cPickle
cStringIO
calendar
cd
cfmfile
cgi
cgitb
chunk
cmath
cmd
code
codecs
codeop
colorsys
commands
compileall
copy
copy_reg
crypt
ctb
curses
curses.ascii
curses.panel
curses.textpad
curses.wrapper
dbhash
dbm
difflib
dircache
dis
distutils
dl
doctest
dumbdbm
email
errno
fcntl
filecmp
fileinput
findertools
fl
flp
fm
fnmatch
formatter
fpectl
fpformat
ftplib
gc
gdbm
getopt
getpass
gettext
gl
glob
gopherlib
grp
gzip
hmac
htmlentitydefs
htmllib
httplib
ic
icopen
imageop
imaplib
imgfile
imghdr
imp
inspect
jpeg
keyword
linecache
locale
mac
macerrors
macfs
macfsn
macostools
macpath
macresource
macspeech
mactty
mailbox
mailcap
marshal
math
md5
mhlib
mimetools
mimetypes
mimify
mkcwproject
mmap
mpz
msvcrt
multifile
mutex
netrc
new
nis
nntplib
nsremote
operator
os
os.path
parser
pickle
pipes
popen2
poplib
posix
posixfile
pprint
preferences
pty
pwd
py_compile
py_resource
pyclbr
pydoc
pythonprefs
quietconsole
quopri
random
re
readline
repr
resource
rexec
rfc822
rgbimg
rlcompleter
robotparser
rotor
sched
select
sgmllib
sha
shelve
shlex
shutil
signal
site
smtplib
sndhdr
socket
stat
statcache
statvfs
string
struct
sunau
sunaudiodev
symbol
sys
syslog
tabnanny
telnetlib
tempfile
termios
thread
threading
time
token
tokenize
traceback
tty
turtle
types
unicodedata
unittest
urllib
urllib2
urlparse
user
uu
videoreader
warnings
waste
wave
weakref
webbrowser
whichdb
whrandom
winsound
xdrlib
xml.dom
xml.dom.minidom
xml.dom.pulldom
xml.parsers.expat
xml.sax
xml.sax.handler
xml.sax.saxutils
xml.sax.xmlreader
xmllib
xmlrpclib
xreadlines
zipfile
zlib""".split()

    for m in mods:
        cursor.execute("DELETE FROM searchIndex where name = '{}' and path like '%#SECTION%'".format(m))


def generate():

    db = sqlite3.connect(DBPATH)
    cursor = db.cursor()
    records = parseModules(DOCPATH)

    cursor.executemany('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', records)
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    generate()
