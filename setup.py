from setuptools import setup

VERSION = '1.3.0'

setup(
    name='pkgconfig',
    version=VERSION,
    author='Matthias Vogelgesang',
    author_email='matthias.vogelgesang@gmail.com',
    url='http://github.com/matze/pkgconfig',
    license='MIT',
    packages=['pkgconfig'],
    description="Interface Python with pkg-config",
    long_description=open('README.rst').read(),
    tests_require=['nose>=1.0'],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*',
    test_suite='test',
)
