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

import requests
from bs4 import BeautifulSoup

from archive_controller import ArchiveController

def defaultInfoFcn(s='Testing printing...', exception=False):
    if exception:
        logger.exception(s)
    else:
        logger.info(s)

class MangafoxModel():
    def __init__(self, series_url, gui_info_fcn=defaultInfoFcn):
        self.gui_info_fcn = gui_info_fcn
        self.series_url = series_url

    def getChaptersList(self):
        r = requests.get(self.series_url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)

        div_ch = soup.body.find('div', attrs={'id':'chapters'})
        blocks = div_ch.findAll('ul', attrs={'class':'chlist'})
        chs = []
        for b in blocks:
            if b.findAll('h3') is not None:
                chs += b.findAll('h3')
            if b.findAll('h4') is not None:
                chs += b.findAll('h4')

        processed_chapters = []
        for ch in chs:
            name = ch.text.replace('\n', ' ').strip()
            href = ch.find('a').get('href')
            processed_chapters.append([name, href])
            
        processed_chapters.reverse()
        
        return processed_chapters
        
    def downloadChapter(self, chapter):
        """
        chapter = [name, url]
        """
        full_gallery_url = chapter[1]
        cut_gallery_url = '/'.join(chapter[1].split('/')[:-1])+'/'
        
        r = requests.get(cut_gallery_url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        
        # parse html
        ch_name = chapter[0]
        grp_name = ''
        
        pages = []
        select = soup.body.find('select', attrs={'class':'m'})
        select_options = select.findAll('option')
        for o in select_options:
            try:
                int(o.text)
            except:
                continue
            pages.append(cut_gallery_url+o.text+'.html')
    
        galery_size = len(pages)
        galeryurl = full_gallery_url 

        logger.info('Downloading: '+ch_name)
        logger.info('Pages: '+str(galery_size))
        logger.info('Images url: '+galeryurl)

        # create temp folder for downloads
        ac = ArchiveController()
        ac.mkdir()

        errors = 0
        for i in range(len(pages)):
            logger.info("Downloading "+str(i+1)+"/"+str(len(pages)))
            self.gui_info_fcn("Downloading "+str(i+1)+"/"+str(len(pages)))
            
            try:
                r = requests.get(pages[i], timeout=30)
            except Exception, e:
                logger.exception('BAD page download for: '+pages[i])
                errors+=1
                continue
            
            html = unicode(r.text)
            soup = BeautifulSoup(html)
            
            img_url = soup.body.find('img', attrs={'id':'image'}).get('src')
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
                errors+=1
            else:
                logger.info('OK download')
                    


        logger.info("Download finished, Failed downloads = "+str(errors))
        
        if grp_name != '':
            grp_name = '_['+grp_name+']'
        archive_name = ac.sanitize_filename(ch_name+grp_name+'.zip')
        
        self.gui_info_fcn('Compressing to: '+str(archive_name))
        logger.info('Compressing to: '+str(archive_name))
        ac.zipdir(archive_name)
        
        ac.rmdir()
        
        if errors>0:
            return False
        else:
            return True
        

