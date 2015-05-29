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

from batoto_model import BatotoModel
from kissmanga_model import KissmangaModel
from mangafox_model import MangafoxModel
from mangatraders_model import MangatradersModel

class DownloadController():
    def __init__(self, gui_info_fcn=None):
        self.gui_info_fcn = gui_info_fcn
        self.webpage_model = None
        self.chapters = []
        self.results = []
        
        self.downloadPath = None
        self.setDownloadPath('.')
        
    def guiInfoFcn(self, s='Testing printing...', exception=False, downloadProgress=False):
        """
        Used to add ability to use keywords to pyqt signals
        """
        if self.gui_info_fcn is None:
            if downloadProgress:
                s = "Downloading progress: "+s
            if exception:
                logger.exception(s)
            else:
                logger.info(s)
        else:
            self.gui_info_fcn(s, exception, downloadProgress)
    
    def setGuiInfoFcn(self, fcn):
        self.gui_info_fcn = fcn
        
    def setDownloadPath(self, path):
        if os.path.isdir(path):
            self.downloadPath = os.path.abspath(path)
            return True
        else:
            return False
            
    def getDownloadPath(self):
        return self.downloadPath
    
    def setSeriesUrl(self, url):
        logger.debug('Set series url: '+url)
        
        if ("bato.to" in url) or ("batoto.com" in url):
            self.webpage_model = BatotoModel(url, self.guiInfoFcn)
            self.guiInfoFcn('Detected batoto url')
        elif "kissmanga.com" in url:
            self.webpage_model = KissmangaModel(url, self.guiInfoFcn)
            self.guiInfoFcn('Detected kissmanga.com url')
        elif "mangafox.me" in url:
            self.webpage_model = MangafoxModel(url, self.guiInfoFcn)
            self.guiInfoFcn('Detected mangafox.me url')
        elif "mangatraders.org" in url:
            self.webpage_model = MangatradersModel(url, self.guiInfoFcn)
            self.guiInfoFcn('Detected mangatraders.org url')
        else:
            self.webpage_model = None
            self.chapters = []
            logger.debug('Unsupported url!')
            self.guiInfoFcn('Unsupported url!')
            return False
        
        try:
            self.chapters = self.webpage_model.getChaptersList()
        except Exception,e:
            self.webpage_model = None
            self.chapters = []
            self.guiInfoFcn('Error when downloading list of chapters! wrong url?', True)
            return False
            
        return True
        
    def getChaptersList(self):
        return self.chapters
        
    def downloadChapter(self, chapter_list_number):
        # list [name, url]
        chapter = self.chapters[chapter_list_number]
        self.guiInfoFcn('Downloading: '+chapter[0])
        
        r = self.webpage_model.downloadChapter(chapter, self.downloadPath)
        
        if not r:
            self.guiInfoFcn('Download finished with errors')
        return r
        
    def downloadChapterRange(self, ch_from, ch_to):
        results = []
        for c_id in range(ch_from, ch_to+1):
            # Downloading progress: x/y
            self.guiInfoFcn(str(c_id+1-ch_from)+'/'+str(ch_to+1-ch_from), downloadProgress=True)
            
            r = self.downloadChapter(c_id)
            results.append(r)
        
        self.results = results
        
        
