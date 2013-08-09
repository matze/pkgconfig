# -*- coding: utf-8 -*-
# Copyright (c) 2013 Matthias Vogelgesang <matthias.vogelgesang@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""pkgconfig is a Python module to interface with the pkg-config command line
tool."""

import subprocess
import re


def _compare_versions(v1, v2):
    """
    Compare two version strings and return -1, 0 or 1 depending on the equality
    of the subset of matching version numbers.

    The implementation is taken from the top answer at
    http://stackoverflow.com/a/1714190/997768.
    """
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    n1 = normalize(v1)
    n2 = normalize(v2)

    return (n1 > n2) - (n1 < n2)


def _split_version_specifier(spec):
    """Splits version specifiers in the form ">= 0.1.2" into ('0.1.2', '>=')"""
    m = re.search(r'([<>=]?=?)?\s*((\d*\.)*\d*)', spec)
    return m.group(2), m.group(1)


def _convert_error(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OSError:
            raise EnvironmentError("pkg-config is not installed")

    return _wrapper


@_convert_error
def _query(package, option):
    cmd = 'pkg-config {0} {1}'.format(option, package).split()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    return out.rstrip().decode('utf-8')


@_convert_error
def exists(package):
    """Return True if package information is available."""
    cmd = 'pkg-config --exists {0}'.format(package).split()
    return subprocess.call(cmd) == 0


@_convert_error
def requires(package):
    """Return a list of package names that is required by the package"""
    return _query(package, '--print-requires').split('\n')


def cflags(package):
    """Return the CFLAGS string returned by pkg-config."""
    return _query(package, '--cflags')


def libs(package):
    """Return the LDFLAGS string returned by pkg-config."""
    return _query(package, '--libs')


def installed(package, version):
    """
    Check if the package meets the required version.

    The version specifier consists of an optional comparator (one of =, ==, >,
    <, >=, <=) and an arbitrarily long version number separated by dots. The
    should be as you would expect, e.g. for an installed version '0.1.2' of
    package 'foo':

    >>> installed('foo', '==0.1.2')
    True
    >>> installed('foo', '<0.1')
    False
    >>> installed('foo', '>= 0.0.4')
    True
    """
    if not exists(package):
        return False

    number, comparator = _split_version_specifier(version)
    modversion = _query(package, '--modversion')

    try:
        result = _compare_versions(modversion, number)
    except ValueError:
        msg = "{0} is not a correct version specifier".format(version)
        raise ValueError(msg)

    if comparator in ('', '=', '=='):
        return result == 0

    if comparator == '>':
        return result > 0

    if comparator == '>=':
        return result >= 0

    if comparator == '<':
        return result < 0

    if comparator == '<=':
        return result <= 0
