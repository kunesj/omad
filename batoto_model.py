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

import requests
from bs4 import BeautifulSoup

from archive_controller import ArchiveController

def defaultInfoFcn(s='Testing printing...', exception=False):
    if exception:
        logger.exception(s)
    else:
        logger.info(s)

class BatotoModel():
    def __init__(self, series_url, gui_info_fcn=defaultInfoFcn):
        self.gui_info_fcn = gui_info_fcn
        self.series_url = series_url

    def getChaptersList(self):
        r = requests.get(self.series_url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)

        table_ch = soup.body.find('table', attrs={'class':'ipb_table chapters_list'})
        en_chs = table_ch.findAll('tr', attrs={'class':'row lang_English chapter_row'})

        processed_chapters = []
        for ch in en_chs:
            tds = ch.findAll('td')
            name = tds[0].text.strip()
            href = tds[0].find('a').get('href')
            processed_chapters.append([name, href])
            
        processed_chapters.reverse()
        
        return processed_chapters
        
    def downloadChapter(self, chapter):
        """
        chapter = [name, url]
        """
        full_gallery_url = chapter[1]
            
        # strip page number etc..
        fgu_spl = full_gallery_url.split('/_/')
        full_gallery_url = fgu_spl[0]+'/_/'+'/'.join(fgu_spl[1].split('/')[:2])
        
        r = requests.get(full_gallery_url+'?supress_webtoon=t', timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        
        # parse html
        div_modbar = soup.body.find('div', attrs={'class':'moderation_bar rounded clear'})

        series_name = div_modbar.find('a').text.replace('/',' ')
        ch_select = div_modbar.find('select', attrs={'name':'chapter_select'})
        ch_name = (series_name+' - '+ch_select.find('option', attrs={'selected':'selected'}).text).replace(' ','_').encode('utf-8')
        
        grp_select = div_modbar.find('select', attrs={'name':'group_select'})
        grp_name = (grp_select.find('option', attrs={'selected':'selected'}).text).encode('utf-8')
        # remove language from group
        grp_name = '-'.join(grp_name.split('-')[:-1]).strip().replace(' ','_')

        pages = div_modbar.find('select', attrs={'name':'page_select'}).text.lower().split('page')[1:]
        pages = [x.strip() for x in pages]
        galery_size = len(pages)

        img_url = soup.body.find('img', attrs={'id':'comic_page'}).get('src')
        galeryurl =  img_url[0:img_url.rfind('/')]+"/"
            

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
                
            p = pages[i]
            page_url = full_gallery_url+'/'+str(p)+'?supress_webtoon=t'
            logger.info("Page url: "+page_url)
            
            try:
                r = requests.get(page_url, timeout=30)
            except Exception, e:
                logger.exception('BAD page download for: '+page_url)
                errors+=1
                continue
                
            html = unicode(r.text)
            soup = BeautifulSoup(html)
            
            img_url = soup.body.find('img', attrs={'id':'comic_page'}).get('src')
            img_ext = img_url.split('.')[-1]
                
            
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
        archive_name = (ch_name+grp_name+'.zip').replace('/','-')
        self.gui_info_fcn('Compressing to: '+str(archive_name))
        logger.info('Compressing to: '+str(archive_name))
        ac.zipdir(archive_name)
        
        ac.rmdir()
        
        if errors>0:
            return False
        else:
            return True
        
