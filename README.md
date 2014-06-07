Python 2.2.1 documentation in Dash format
=========================================

The Jython implementation shipped with WebLogic and WebSphere is stuck at 2.2.1, so 
if you have to work with it, it's nice to have this particular documentation in Dash.

This script will download and repackage the docs as necessary.

If you trust me enough to accept automatic updates instead, have a look at 
[my blog post](http://blog.pythonaro.com/2014/06/dash-docset-for-python-221-ie-jython.html) 
for instructions on how to add my Python 2.2.1 feed to your Dash.

Requirements
------------

* Python 3.x (tested with 3.3)
* BeautifulSoup4 (you can install it with `pip install -r requirements.txt` )


HOWTO
-----

1. `python mkdash.py`
2. launch Dash, go to `Dash -> Preferences... -> Docsets`, click `+` and point to python221.docset

Feedback
--------

Feel free to open issues here on Github or ping @toyg on Twitter or Twister

References
----------

* http://kapeli.com/docsets


