#!/usr/bin/python2
# coding: utf-8
"""
This file is part of Manga Downloader.

Manga Downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

Manga Downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Manga Downloader.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
logger = logging.getLogger(__name__)
import traceback

import os
import shutil
from random import randint
import zipfile

import requests

class ArchiveController():
    def __init__(self, rootpath='./'):
        self.rootpath = rootpath
        self.foldername = None
        self.path = None
    
    def mkdir(self):
        # create temp folder for downloads
        foldername="_temp"
        while os.path.exists(os.path.join(self.rootpath, foldername)):
            foldername=foldername+str(randint(0,9))
        os.makedirs(os.path.join(self.rootpath, foldername))
        self.foldername = foldername
        self.path = os.path.join(self.rootpath, self.foldername)
        
    def rmdir(self):
        shutil.rmtree(self.path)
        self.foldername = None
        self.path = None
        
    def zipdir(self, archive_name, archive_path='./'):
        archive_name = self.sanitize_filename(archive_name)
        zipf = zipfile.ZipFile(os.path.join(archive_path, archive_name), 'w')
        for root, dirs, files in os.walk(self.path):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()
        
    def sanitize_filename(self, filename):
        # strip white characters from start/end
        filename = filename.strip()

        # replace ntfs illegal characters
        illegal = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for ch in illegal:
            if ch in filename:
                filename = filename.replace(ch, "_")
                
        # replace tab with space
        filename = filename.replace("\t", " ")
        
        return filename
                
    def download(self, url, filename):
        f = open(os.path.join(self.path, filename),'wb')
        f.write(requests.get(url, timeout=30).content)
        f.close()

        
