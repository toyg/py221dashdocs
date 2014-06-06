Python 2.2.1 documentation in Dash format
=========================================

The Jython implementation shipped with WebLogic and WebSphere is stuck at 2.2.1, so 
if you have to work with it, it's nice to have this particular documentation in Dash.

This script will do most of the work for you.

Requirements
------------

* Python 3.x (tested with 3.3)
* BeautifulSoup4 (you can install it with `pip install -r requirements.txt` )


HOWTO
-----

1. Download the original HTML docs from https://www.python.org/ftp/python/doc/2.2.1/
2. unzip it in py221dashdocs/python221.docset/Contents/Resources
3. rename the resulting directory "html-2.2.1" to "Documents"
4. `python mkdash.py`
5. launch Dash, go to `Dash -> Preferences... -> Docsets`, click `+` and point to python221.docset

Feedback
--------

Feel free to open issues here on Github or ping @toyg on Twitter or Twister

References
----------

* http://kapeli.com/docsets


