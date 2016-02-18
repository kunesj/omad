#!/usr/bin/python2
# coding: utf-8
"""
This file is part of OMAD.

OMAD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

OMAD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OMAD.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
logger = logging.getLogger(__name__)
import traceback

import os
import tempfile
import shutil
from random import randint
import zipfile

import requests

class ArchiveController():
    def __init__(self, downloadPath='./'):
        self.path = None
        self.downloadPath = downloadPath
    
    def mkdir(self):
        self.path = tempfile.mkdtemp()
        
    def rmdir(self):
        shutil.rmtree(self.path)
        self.path = None
        
    def zipdir(self, archive_name):
        archive_name = self.sanitize_filename(archive_name)
        archive_path = os.path.join(self.downloadPath, archive_name)
        logger.debug('Compressing files in temp folder to archive in path: '+archive_path)
        
        zipf = zipfile.ZipFile(archive_path, 'w')
        for root, dirs, files in os.walk(self.path):
            for file in files:
                full_path = os.path.join(root, file)
                if os.path.isfile(full_path):
                    zipf.write(full_path, os.path.basename(full_path))
        zipf.close()
        
    def sanitize_filename(self, filename, replaceSpaces=True):
        # strip white characters from start/end
        filename = filename.strip()

        # replace ntfs illegal characters
        illegal = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for ch in illegal:
            if ch in filename:
                filename = filename.replace(ch, "_")
                
        # replace tab with space
        filename = filename.replace("\t", " ")
        
        # optionaly replace spaces with _
        filename = filename.replace(' ', '_')
        
        return filename
                
    def download(self, url, filename):
        response = requests.get(url, timeout=30)
        if response.status_code == 503:
            raise Exception("503 Service Unavailable")
        
        with open(os.path.join(self.path, filename),'wb') as f:
            f.write(response.content)

        
