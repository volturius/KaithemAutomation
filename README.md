KaithemAutomation
=================

Flexible home/commercial automation server written in python, HTML, Mako, and CSS.

KAITHEM WAS NOT DESIGNED FOR MILITARY, AEROSPACE, IDUSTRIAL,
MEDICAL, NUCLEAR, SAFETY OF LIFE OR ANY OTHER CRITICAL APPLICATION
ESPECIALLY THE CURRENT STILL-IN-DEVELOPMENT VERSION. YOU PROBABLY SHOULDN'T TRUST IT FOR
A SECURITY SYSTEM FOR A BAG OF FUNYUNS(tm) AT THIS POINT! 

Installation
============

All dependancies should already be included. Huge thanks to the developers of Mako, cherrypy, ace code editor, and pyYAML

git clone or download somewhere and run python3 kaithem/kaithem.py
You can also use python2 if you really want.

Command line options:
    "-c"
        Supply a specific configuration file. Otherwise uses default. Any option not found in supplied file
        Reverts to default the files are YAML, see kaithem/data/default_configuration.txt for info on options.
        
    "-p"
        Specify a port. Overrides all config stuff.


Then point your browser to https://localhost:<yourport> (default port is 8001)
and log in with Username:admin Password:password

It will give you a security warning, that the SSL certificate name is wrong,
ignore if you are just playing around, use real SSL keys otherwise.

Look at the help section and the examples module, there is a lot more documentation built into the system.

If you are really going to use this you must change the ssl keys in /ssl to something actually secret.


License Terms
=============
The original python code and and the HTML files under /pages are licensed under the GNU GPL v3.
However, Kaithem includes code copied unmmodifed from Mako and Cherrypy, two excellent open source projects.
Those projects remain under their respective licenses.

Some images used in theming are taken from this site: http://webtreats.mysitemyway.com/ and may be considered non-free
by some due to a restriction on "redistribution as-is for free in a manner that directly competes with our own websites."
However they are royalty free for personal and commercial use ad do not require attribution, So I consider them appropriate
for an open project

