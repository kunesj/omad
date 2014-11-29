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

import os
from os import system
import shutil
from random import randint
import zipfile

import requests
from bs4 import BeautifulSoup

def defaultInfoFcn(s='Testing printing...'):
    logger.info(s)

class KissmangaModel():
    def __init__(self, series_url, gui_info_fcn=defaultInfoFcn):
        self.gui_info_fcn = gui_info_fcn
        self.series_url = series_url
        
    def getChaptersList(self):
        r = requests.get(self.series_url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)

        table_ch = soup.body.find('table', attrs={'class':'listing'})
        en_chs = table_ch.findAll('a')

        processed_chapters = []
        for ch in en_chs:
            name = ch.get('title').strip()
            href = ch.get('href')
            if not 'kissmanga.com' in href:
                href = 'http://kissmanga.com/'+href
            processed_chapters.append([name, href])
            
        processed_chapters.reverse()
        
        return processed_chapters
        
    def zipdir(self, path, zipf):
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file))
                
    def download(self, url, path):
        f = open(path,'wb')
        f.write(requests.get(url).content)
        f.close()
        
    def downloadChapter(self, chapter):
        """
        chapter = [name, url]
        """
        full_gallery_url = chapter[1]
        
        r = requests.get(full_gallery_url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        
        # parse html
        series_name = full_gallery_url.split('/Manga/')[-1].split('/')[0]
        ch_name = (series_name+' - '+full_gallery_url.split('/')[-1].split('?')[0]).replace(' ','_').encode('utf-8')
        grp_name = ''
        
        pages = []
        scripts = soup.body.findAll('script', attrs={'type':'text/javascript'})
        for script in scripts:
            if script.text.strip().startswith('var lstImages = new Array();'):
                lines = script.text.split('\n')
                for l in lines:
                    if l.strip().startswith('lstImages.push('):
                        pages.append(l.strip().split('lstImages.push("')[-1].split('");')[0])
        
        galery_size = len(pages)
        galeryurl = full_gallery_url
            

        logger.info('Downloading: '+ch_name)
        logger.info('Pages: '+str(galery_size))
        logger.info('Images url: '+galeryurl)

        # create temp folder for downloads
        foldername="_temp"
        while os.path.exists('./'+foldername):
            foldername=foldername+str(randint(0,9))
        os.makedirs('./'+foldername)

        errors = 0
        for i in range(len(pages)):
            logger.info("Downloading "+str(i+1)+"/"+str(len(pages)))
            self.gui_info_fcn("Downloading "+str(i+1)+"/"+str(len(pages)))
                
            img_url = pages[i]
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
            img_path = './'+foldername+'/'+img_filename
            
            try:
                self.download(img_url, img_path)
            except Exception, e:
                logger.warning('BAD download for: '+img_url)
                logger.warning(e)
                errors+=1
            else:
                logger.info('OK download')
                    


        logger.info("Download finished, Failed downloads = "+str(errors))
        
        if grp_name != '':
            grp_name = '_['+grp_name+']'
        archive_name = (ch_name+grp_name+'.zip').replace('/','-')
        logger.info('Compressing to: '+str(archive_name))
        zipf = zipfile.ZipFile(archive_name, 'w')
        self.zipdir('./'+foldername, zipf)
        zipf.close()

        shutil.rmtree('./'+foldername)
        
        if errors>0:
            return False
        else:
            return True
        

