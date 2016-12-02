from setuptools import setup

VERSION = '1.2.2'

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
    setup_requires=['nose>=1.0'],
    test_suite='test',
)
