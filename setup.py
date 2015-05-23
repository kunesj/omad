#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

setup(name='omad',
        version='0.1',
        description='Online MAnga Downloader, simple application for downloading chapters from online manga reading sites.',
        long_description=open("README.md").read(),
        author='Jiří Kuneš',
        author_email='jirka642@gmail.com',
        url='https://github.com/kunesj/omad',
        packages=['omad'],
        include_package_data=True,
        license="GPL3",
        entry_points={
        'console_scripts': ['omad = omad.omad_app:main'],
        },
        install_requires=[
          'beautifulsoup',
          'requests'
          # python-qt4 
        ],
    )
