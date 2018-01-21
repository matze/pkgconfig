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
        nt.assert_true(flag in ('-L/usr/lib_gtk_foo', '-lgtk-3'))


def test_parse():
    config = pkgconfig.parse("fake-gtk+-3.0 fake-python")

    nt.assert_true(('GSEAL_ENABLE', None) in config['define_macros'])
    nt.assert_true('/usr/include/gtk-3.0' in config['include_dirs'])
    nt.assert_true('/usr/lib_gtk_foo' in config['library_dirs'])
    nt.assert_true('/usr/lib_python_foo' in config['library_dirs'])
    nt.assert_true('gtk-3' in config['libraries'])

    nt.assert_true('/usr/include/python2.7' in config['include_dirs'])


def test_listall():
    packages = pkgconfig.list_all()
    nt.assert_true('fake-gtk+-3.0' in packages)
    nt.assert_true('fake-python' in packages)


def test_variables():
    variables = pkgconfig.variables('fake-python')

    nt.assert_true('prefix' in variables)
    nt.assert_true('exec_prefix' in variables)
    nt.assert_true('libdir' in variables)
    nt.assert_true('includedir' in variables)

    nt.assert_true(variables['prefix'] == '/usr')
    nt.assert_true(variables['exec_prefix'] == '/usr')
    nt.assert_true(variables['libdir'] == '/usr/lib_python_foo')
    nt.assert_true(variables['includedir'] == '/usr/include')
