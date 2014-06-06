# -*- coding: utf-8 -*-
__author__ = 'Giacomo Lacava'

import sqlite3
from os.path import join, dirname
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


def generate():

    db = sqlite3.connect(DBPATH)
    cursor = db.cursor()

    # create base table
    try:
        cursor.execute('DROP TABLE searchIndex;')
    except:
        pass   # table was not there
    cursor.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cursor.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    # populate
    records = parseModules(DOCPATH)
    cursor.executemany('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', records)

    # For various reasons, a lot of entries with "#SECTION..." are duplicated, but not all.
    mods = []
    with open('dupes.txt', 'r', encoding='utf-8') as df:
        mods = [m.strip() for m in df.readlines()]
    for m in mods:
        cursor.execute("DELETE FROM searchIndex where name = '{}' and path like '%#SECTION%'".format(m))

    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    generate()
    print("All done.")
