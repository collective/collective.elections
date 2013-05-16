# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import os

version = '1.0'
long_description = open("README.txt").read() + "\n" + \
    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
    open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
    open(os.path.join("docs", "HISTORY.txt")).read()

setup(
    name='collective.elections',
    version=version,
    description="An implementation of the KOA electronic voting system for Plone.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone dexterity koa gnupg openpgp',
    author='Héctor Velarde',
    author_email='hector.velarde@gmail.com',
    url='https://github.com/collective/collective.elections',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'borg.localrole',
        'Pillow',
        'plone.app.dexterity',
        'plone.principalsource',
        'python-gnupg',
        'setuptools',
        'xhtml2pdf',
    ],
    extras_require={
        'test': ['plone.app.testing'],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
