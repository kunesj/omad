#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

setup(name='manga_downloader',
        version='0.1',
        description='Simple application for downloading chapters from online manga reading sites.',
        long_description=open("README.md").read(),
        author='Jiří Kuneš',
        author_email='jirka642@gmail.com',
        url='https://github.com/kunesj/manga_downloader',
        packages=['mangadownloader'],
        include_package_data=True,
        license="GPL3",
        entry_points={
        'console_scripts': ['mangadownloader = mangadownloader.mangadownloader_app:main'],
        },
        install_requires=[
          'beautifulsoup',
          'requests'
          # python-qt4 
        ],
    )
