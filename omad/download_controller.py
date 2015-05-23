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

from batoto_model import BatotoModel
from kissmanga_model import KissmangaModel
from mangafox_model import MangafoxModel
from mangatraders_model import MangatradersModel

def defaultInfoFcn(s='Testing printing...', exception=False):
    if exception:
        logger.exception(s)
    else:
        logger.info(s)

class DownloadController():
    def __init__(self, gui_info_fcn=defaultInfoFcn):
        self.gui_info_fcn = gui_info_fcn
        self.webpage_model = None
        self.chapters = []
        self.results = []
    
    def setSeriesUrl(self, url):
        if ("bato.to" in url) or ("batoto.com" in url):
            self.webpage_model = BatotoModel(url, self.gui_info_fcn)
            self.gui_info_fcn('Detected batoto url')
        elif "kissmanga.com" in url:
            self.webpage_model = KissmangaModel(url, self.gui_info_fcn)
            self.gui_info_fcn('Detected kissmanga.com url')
        elif "mangafox.me" in url:
            self.webpage_model = MangafoxModel(url, self.gui_info_fcn)
            self.gui_info_fcn('Detected mangafox.me url')
        elif "mangatraders.org" in url:
            self.webpage_model = MangatradersModel(url, self.gui_info_fcn)
            self.gui_info_fcn('Detected mangatraders.org url')
        else:
            self.webpage_model = None
            self.chapters = []
            logger.debug('Unsupported url!')
            self.gui_info_fcn('Unsupported url!')
            return False
        
        try:
            self.chapters = self.webpage_model.getChaptersList()
        except Exception,e:
            self.webpage_model = None
            self.chapters = []
            self.gui_info_fcn('Error when downloading list of chapters! wrong url?', True)
            return False
            
        return True
        
    def getChaptersList(self):
        return self.chapters
        
    def downloadChapter(self, chapter_list_number):
        # list [name, url]
        chapter = self.chapters[chapter_list_number]
        self.gui_info_fcn('Downloading: '+chapter[0])
        
        r = self.webpage_model.downloadChapter(chapter)
        
        if not r:
            self.gui_info_fcn('Download finished with errors')
        return r
        
    def downloadChapterRange(self, ch_from, ch_to):
        results = []
        for c_id in range(ch_from, ch_to+1):
            self.gui_info_fcn('Downloading progress: '+str(c_id+1-ch_from)+'/'+str(ch_to+1-ch_from))
            r = self.downloadChapter(c_id)
            results.append(r)
        
        self.results = results
        
        
