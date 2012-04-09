# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.elections',
      version=version,
      description="A voting system for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity koa gnupg openpgp',
      author='Héctor Velarde',
      author_email='hector.velarde@gmail.com',
      url='https://github.com/collective/collective.elections',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'python-gnupg',
        'plone.app.dexterity>=1.2.1',
        'plone.principalsource',
        'borg.localrole',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
