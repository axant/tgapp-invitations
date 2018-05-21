# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires=[
    "TurboGears2 >= 2.3.9",
    "tgext.pluggable >= 0.7.1",
    "axf",
    "sprox",
    "tgapp-registration >= 0.9.0",
]

testpkgs = [
    'WebTest >= 1.2.3',
    'nose',
    'coverage',
    'ming >= 0.6.1',
    'sqlalchemy',
    'zope.sqlalchemy',
    'repoze.who',
    'tw2.forms',
    'kajiki',
    'tgext.evolve',
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-invitations',
    version='0.2.7',
    description='Provides a way to invite new users into a TurboGears2 application',
    long_description=README,
    author='Axant, Vincenzo Castiglia',
    author_email='vincenzo.castiglia@axant.it',
    url='https://github.com/axant/tgapp-invitations',
    keywords='turbogears2.application',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'invitations': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'invitations': [
            ('**.py', 'python', None),
            ('templates/**.xhtml', 'kajiki', None),
            ('public/**', 'ignore', None)
    ]},
    entry_points="""
    """,
    zip_safe=False,
    extras_require={
        'testing': testpkgs,
    },
)
