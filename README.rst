pkgconfig
=========

.. image:: https://travis-ci.org/matze/pkgconfig.png?branch=master
    :target: https://travis-ci.org/matze/pkgconfig

``pkgconfig`` is a Python module to interface with the ``pkg-config``
command line tool and supports Python 2.6+.

It can be used to

-  check if a package exists ::

       >>> pkgconfig.exists('glib-2.0')
       True

-  check if a package meets certain version requirements ::

       >>> pkgconfig.installed('glib-2.0', '< 2.26')
       False

-  query CFLAGS and LDFLAGS ::

       >>> pkgconfig.cflags('glib-2.0')
       '-I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include'

       >>> pkgconfig.libs('glib-2.0')
       '-lglib-2.0'

-  parse the output to build extensions with setup.py ::

       >>> d = pkgconfig.parse('glib-2.0')
       >>> d['libraries']
       set([u'glib-2.0'])

The ``pkgconfig`` module is licensed under the MIT license.
