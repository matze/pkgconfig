from setuptools import setup

VERSION = '1.4.0'

setup(
    name='pkgconfig',
    version=VERSION,
    author='Matthias Vogelgesang',
    author_email='matthias.vogelgesang@gmail.com',
    url='https://github.com/matze/pkgconfig',
    license='MIT',
    packages=['pkgconfig'],
    description="Interface Python with pkg-config",
    long_description=open('README.rst').read(),
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Build Tools',
    ],
    tests_require=['pytest >= 3.8.2'],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*',
    test_suite='test',
)
