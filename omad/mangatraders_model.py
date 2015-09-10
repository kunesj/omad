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

import requests
import urlparse
try:
    from BeautifulSoup import BeautifulSoup
except:
    # windows fix
    from bs4 import BeautifulSoup 

from archive_controller import ArchiveController


class MangatradersModel():
    """
    Example usage:

    if __name__ == "__main__":
        logging.basicConfig()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        from download_controller import DownloadController
        dc = DownloadController()
        
        mod = MangatradersModel('http://mangatraders.org/manga/?series=CromartieHighSchool&uploader=LeturLefr', dc.guiInfoFcn)
        chapters = mod.getChaptersList()
        print chapters[0]
        print mod.downloadChapter(chapters[0], './')
    """

    def __init__(self, series_url, gui_info_fcn):
        # default is download_controller.defaultInfoFcn
        self.gui_info_fcn = gui_info_fcn
        
        # fix url
        params = urlparse.parse_qs(urlparse.urlparse(series_url).query)
        if 'series' in params:
            series_url = 'http://mangatraders.org/read-online/'+params['series'][0]
            logger.info('Series url autochanged to: '+series_url)
        self.series_url = series_url
        
    def getChaptersList(self):
        r = requests.get(self.series_url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        
        rows = soup.body \
                .find('div', attrs={'class':'container mainContainer'}) \
                .find('div', attrs={'class':'well'}) \
                .findAll('div', attrs={'class':'row', 'style':'margin-bottom:10px;'})
            
        processed_chapters = []
        for r in rows:
            a = r.find('a')
            name = a.text.strip()
            name = BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).text
            href = a.get('href')
            if not 'mangatraders.org' in href:
                href = 'http://mangatraders.org'+href
            processed_chapters.append([name, href])
            
        processed_chapters.reverse()
        
        return processed_chapters
    
    def downloadChapter(self, chapter, downloadPath):
        return self.downloadChapter_online(chapter, downloadPath)
        # TODO - if logged in, use direct download
    
    def downloadChapter_online(self, chapter, downloadPath):
        """        
        chapter = [name, url]
        
        Downloads chapter in online reading mode, does not need login
        """
        full_gallery_url = chapter[1]
        
        try:
            cut_gallery_url = full_gallery_url.split('/page-')[0]
            
            r = requests.get(full_gallery_url, timeout=30)
            html = unicode(r.text)
            soup = BeautifulSoup(html)
            
            # parse html
            mainPageContainer = soup.body.find('div', attrs={'class':'container mainPageContainer'})
            
            series_name = mainPageContainer.find('ol').find('li').find('a') \
                .text.strip()
            series_name = BeautifulSoup(series_name, convertEntities=BeautifulSoup.HTML_ENTITIES).text
            ch_name = series_name+' - '+mainPageContainer.find('ol') \
                .find('select', attrs={'id':'changeChapterSelect'}) \
                .find('option', attrs={'selected':'selected'}).text.strip()
            ch_name = BeautifulSoup(ch_name, convertEntities=BeautifulSoup.HTML_ENTITIES).text
            grp_name = ''
            
            pages = []
            pages_options = mainPageContainer.find('ol') \
                .find('select', attrs={'id':'changePageSelect'}).findAll('option')
            for p in pages_options:
                pages.append(cut_gallery_url+'/'+p.get('value'))
            
            galery_size = len(pages)
            galeryurl = full_gallery_url
        except Exception, e:
            logger.exception('Failed to parse chapter page for: '+full_gallery_url)
            self.gui_info_fcn("Error downloading/parsing chapter html")
            return False # failed download
            
        logger.info('Downloading: '+ch_name)
        logger.info('Pages: '+str(galery_size))
        logger.info('Images url: '+cut_gallery_url)

        # create temp folder for downloads
        ac = ArchiveController(downloadPath)
        ac.mkdir()

        errors = 0
        for i in range(len(pages)):
            self.gui_info_fcn("Downloading page "+str(i+1)+"/"+str(len(pages)))
            
            r = requests.get(pages[i], timeout=30)
            html = unicode(r.text)
            soup = BeautifulSoup(html)
            
            img_url = soup.body \
                .find('div', attrs={'style':'text-align:center;'}) \
                .find('img').get('src')
            img_ext = img_url.split('.')[-1].split('?')[0]                
            
            logger.info(img_url)
            
            if i<10:
                num = '000'+str(i)
            elif i<100:
                num = '00'+str(i)
            elif i<1000:
                num = '0'+str(i)
            else:
                num = str(i)
            
            img_filename = num+'.'+img_ext
            
            try:
                ac.download(img_url, img_filename)
            except Exception, e:
                logger.exception('BAD download for: '+img_url)
                self.gui_info_fcn("Error downloading page image")
                errors+=1
            else:
                logger.debug('OK download')
                    
        
        logger.info("Download finished, Failed downloads = "+str(errors))
        
        if grp_name != '':
            grp_name = ' ['+grp_name+']'
        archive_name = ac.sanitize_filename(ch_name+grp_name+'.zip')
        
        self.gui_info_fcn('Compressing to: '+archive_name)
        ac.zipdir(archive_name)
        
        ac.rmdir()
        
        if errors>0:
            return False
        else:
            return True
