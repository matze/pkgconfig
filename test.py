import os
import pkgconfig
import nose.tools as nt

os.environ['PKG_CONFIG_PATH'] = os.path.abspath('./data')
PACKAGE_NAME = 'fake-gtk+-3.0'


def test_exists():
    nt.assert_true(pkgconfig.exists(PACKAGE_NAME))


def test_version():
    assertions = {
        '3.2.1': True,
        '==3.2.1': True,
        '==3.2.2': False,
        '> 2.2': True,
        '> 3.4': False,
        '<= 3.3.5': True,
        '< 2.3': False
    }

    for version, val in assertions.items():
        nt.assert_true(pkgconfig.installed(PACKAGE_NAME, version) == val)


def test_cflags():
    flags = pkgconfig.cflags(PACKAGE_NAME)

    for flag in flags.split(' '):
        nt.assert_true(flag in ('-DGSEAL_ENABLE', '-I/usr/include/gtk-3.0'))


def test_libs():
    flags = pkgconfig.libs(PACKAGE_NAME)

    for flag in flags.split(' '):
        nt.assert_true(flag in ('-L/usr/lib64', '-lgtk-3'))
