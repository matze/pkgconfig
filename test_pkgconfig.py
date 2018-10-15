import os
import pytest
import pkgconfig

os.environ['PKG_CONFIG_PATH'] = os.path.abspath('./data')
PACKAGE_NAME = 'fake-gtk+-3.0'


def test_exists():
    assert pkgconfig.exists(PACKAGE_NAME)


@pytest.mark.parametrize("version,expected",[
    ('3.2.1', True),
    ('==3.2.1', True),
    ('==3.2.2', False),
    ('> 2.2', True),
    ('> 3.4', False),
    ('<= 3.3.5', True),
    ('< 2.3', False),
])
def test_version(version, expected):
    assert pkgconfig.installed(PACKAGE_NAME, version) == expected


def test_cflags():
    flags = pkgconfig.cflags(PACKAGE_NAME)

    for flag in flags.split(' '):
        assert flag in ('-DGSEAL_ENABLE', '-I/usr/include/gtk-3.0')


def test_libs():
    flags = pkgconfig.libs(PACKAGE_NAME)

    for flag in flags.split(' '):
        assert flag in ('-L/usr/lib_gtk_foo', '-lgtk-3')


def test_libs_static():
    flags = pkgconfig.libs('fake-python', static=True)
    flags = flags.split(' ')
    assert '-lpthread' in flags
    assert '-ldl' in flags
    assert '-lutil' in flags


def test_parse():
    config = pkgconfig.parse("fake-gtk+-3.0 fake-python")

    assert ('GSEAL_ENABLE', None) in config['define_macros']
    assert '/usr/include/gtk-3.0' in config['include_dirs']
    assert '/usr/lib_gtk_foo' in config['library_dirs']
    assert '/usr/lib_python_foo' in config['library_dirs']
    assert 'gtk-3' in config['libraries']

    assert '/usr/include/python2.7' in config['include_dirs']


def test_parse_static():
    config = pkgconfig.parse("fake-python", static=True)
    assert '/usr/lib_python_foo' in config['library_dirs']
    assert '/usr/include/python2.7' in config['include_dirs']
    assert 'python2.7' in config['libraries']
    assert 'pthread' in config['libraries']
    assert 'dl' in config['libraries']
    assert 'util' in config['libraries']


def test_listall():
    packages = pkgconfig.list_all()
    assert 'fake-gtk+-3.0' in packages
    assert 'fake-python' in packages


def test_variables():
    variables = pkgconfig.variables('fake-python')

    assert 'prefix' in variables
    assert 'exec_prefix' in variables
    assert 'libdir' in variables
    assert 'includedir' in variables

    assert variables['prefix'] == '/usr'
    assert variables['exec_prefix'] == '/usr'
    assert variables['libdir'] == '/usr/lib_python_foo'
    assert variables['includedir'] == '/usr/include'
