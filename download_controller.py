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

from batoto_model import BatotoModel
from kissmanga_model import KissmangaModel

def defaultInfoFcn(s='Testing printing...'):
    logger.info(s)

class DownloadController():
    def __init__(self, gui_info_fcn=defaultInfoFcn):
        self.gui_info_fcn = gui_info_fcn
        self.webpage_model = None
        self.chapters = []
        pass
    
    def setSeriesUrl(self, url):
        if ("bato.to" in url) or ("batoto.com" in url):
            self.webpage_model = BatotoModel(url, self.gui_info_fcn)
            self.gui_info_fcn('Detected batoto url')
        elif "kissmanga.com" in url:
            self.webpage_model = KissmangaModel(url, self.gui_info_fcn)
            self.gui_info_fcn('Detected kissmanga url')
        else:
            self.webpage_model = None
            self.chapters = []
            logger.error(e)
            self.gui_info_fcn('Bad url!')
            return False
        
        try:
            self.chapters = self.webpage_model.getChaptersList()
        except Exception,e:
            self.webpage_model = None
            self.chapters = []
            logger.error(e)
            self.gui_info_fcn('Error when downloading list of chapters! wrong url?')
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
            
        return results
        
        
