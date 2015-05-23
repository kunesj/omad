#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

setup(name='omad',
        version='0.2-pre2',
        description='Online MAnga Downloader, simple application for downloading chapters from online manga reading sites.',
        author='Jiří Kuneš',
        author_email='jirka642@gmail.com',
        url='https://github.com/kunesj/omad',
        download_url = 'https://github.com/kunesj/omad/tarball/v0.2-pre2',
        keywords = ['manga', 'download'],
        packages=['omad'],
        include_package_data=True,
        license="GPL3",
        entry_points={
        'console_scripts': ['omad = omad.omad_app:main'],
        },
        install_requires=[
          'setuptools',
          'beautifulsoup',
          'requests'
          # python-qt4 
        ],
    )
