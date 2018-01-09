#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='wagtailsnippetscopy',
    version='0.1.0',
    description="""'Copy A Snippet' Feature for Wagtail CMS""",
    long_description=readme,
    author='Tim Kamanin',
    author_email='tim@timonweb.com',
    url='https://timonweb.com/oss/wagtailsnippetscopy/',
    packages=[
        'wagtailsnippetscopy',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="The MIT License (MIT)",
    zip_safe=False,
    keywords='wagtail',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
