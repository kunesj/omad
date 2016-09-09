#!/usr/bin/env python3
# encoding: utf-8

import os
from setuptools import setup

import omad

setup(name='omad',
        version = omad.__version__,
        description = 'Online MAnga Downloader, simple application for downloading chapters from online manga reading sites.',
        long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
        author = 'Jiří Kuneš',
        author_email = 'jirka642@gmail.com',
        url = 'https://github.com/kunesj/omad',
        download_url = 'https://github.com/kunesj/omad/tarball/v'+str(omad.__version__),
        keywords = ['manga', 'download'],
        packages = ['omad', 'omad.misctools'],
        include_package_data = True,
        license = "GPL3",
        entry_points = {
        'console_scripts': ['omad = omad.omad_app:main'],
        'gui_scripts': ['omad_gui = omad.omad_app:main'],
        },
        install_requires = [
          'setuptools',
          'beautifulsoup4',
          'requests'
          # python3-qt4 > use apt-get
        ],
    )
