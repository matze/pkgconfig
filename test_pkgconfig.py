from distutils.core import Extension
import os
import pytest
import pkgconfig

os.environ['PKG_CONFIG_PATH'] = os.path.abspath('./data')
PACKAGE_NAME = 'fake-gtk+-3.0'


def test_exists():
    assert pkgconfig.exists(PACKAGE_NAME)
    assert pkgconfig.exists('fake-openssl')


@pytest.mark.parametrize("version,expected", [
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


@pytest.mark.parametrize("version,expected", [
    ('1.1.0j', True),
    ('==1.1.0j', True),
    ('==1.1.0k', False),
    ('>= 1.1.0', True),
    ('> 1.2.0', False),
    ('< 1.2.0', True),
    ('< 1.1.0', False),
    ('>= 1.1', True),
    ('> 1.2', False),
    ('< 1.2', True),
    ('< 1.1', False),
    ('>= 1.1.0c', True),
    ('>= 1.1.0k', False),
    # PLEASE NOTE:
    # the letters have no semantics, except string ordering, see also the
    # comment in the test below.
    # comparing release with beta, like "1.2.3" > "1.2.3b" does not work.
])
def test_openssl(version, expected):
    assert pkgconfig.installed('fake-openssl', version) == expected


@pytest.mark.parametrize("version,expected", [
    ('1.2.3b4', True),
    ('==1.2.3b4', True),
    ('==1.2.3', False),
    ('>= 1.2.3b3', True),
    ('< 1.2.3b5', True),
    # PLEASE NOTE:
    # sadly, when looking at all (esp. non-python) libraries out there, there
    # is no agreement on the semantics of letters appended to version numbers.
    # e.g. for a release candidate, some might use "c", but other also might
    # use "rc" or whatever. stuff like openssl does not use the letters to
    # represent release status, but rather minor updates using a-z.
    # so, as there is no real standard / agreement, we can NOT assume any
    # advanced semantics here (like we could for python packages).
    # thus we do NOT implement any special semantics for the letters,
    # except string ordering
    # thus, comparing a version with a letter-digits appendix to one without
    # may or may not give the desired result.
    # e.g. python packages use a1 for alpha 1, b2 for beta 2, c3 for release
    # candidate 3 and <nothing> for release.
    # we do not implement this semantics, "1.2.3" > "1.2.3b1" does not work.
])
def test_dld_pkg(version, expected):
    assert pkgconfig.installed('fake-dld-pkg', version) == expected


def test_modversion():
    assert pkgconfig.modversion(PACKAGE_NAME) == '3.2.1'
    assert pkgconfig.modversion('fake-openssl') == '1.1.0j'

    with pytest.raises(pkgconfig.PackageNotFoundError):
        pkgconfig.modversion('doesnotexist')


def test_cflags():
    flags = pkgconfig.cflags(PACKAGE_NAME)

    for flag in flags.split(' '):
        assert flag in ('-DGSEAL_ENABLE', '-I/usr/include/gtk-3.0')

    with pytest.raises(pkgconfig.PackageNotFoundError):
        pkgconfig.cflags('doesnotexist')


def test_libs():
    flags = pkgconfig.libs(PACKAGE_NAME)

    for flag in flags.split(' '):
        assert flag in ('-L/usr/lib_gtk_foo', '-lgtk-3')

    with pytest.raises(pkgconfig.PackageNotFoundError):
        pkgconfig.libs('doesnotexist')


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

    with pytest.raises(pkgconfig.PackageNotFoundError):
        pkgconfig.parse('doesnotexist')


def test_parse_static():
    config = pkgconfig.parse("fake-python", static=True)
    assert '/usr/lib_python_foo' in config['library_dirs']
    assert '/usr/include/python2.7' in config['include_dirs']
    assert 'python2.7' in config['libraries']
    assert 'pthread' in config['libraries']
    assert 'dl' in config['libraries']
    assert 'util' in config['libraries']


def test_configure_extension():
    ext = Extension('foo', ['foo.c'])
    pkgconfig.configure_extension(ext, 'fake-gtk+-3.0 fake-python')
    assert sorted(ext.extra_compile_args) == [
         '-DGSEAL_ENABLE', '-I/usr/include/gtk-3.0','-I/usr/include/python2.7']
    assert sorted(ext.extra_link_args) == [
        '-L/usr/lib_gtk_foo', '-L/usr/lib_python_foo', '-lgtk-3', '-lpython2.7']


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

    with pytest.raises(pkgconfig.PackageNotFoundError):
        pkgconfig.variables('doesnotexist')
