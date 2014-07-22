#!/usr/bin/python2
# coding: utf-8
"""
This file is part of Batoto Downloader.

Batoto Downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

Batoto Downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Batoto Downloader.  If not, see <http://www.gnu.org/licenses/>.
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

def zipdir(path, zipf):
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
            
def download(url, path):
    f = open(path,'wb')
    f.write(requests.get(url).content)
    f.close()

def getChapter(full_gallery_url, guiprintfcn=None):
    # strip page number etc..
    fgu_spl = full_gallery_url.split('/_/')
    full_gallery_url = fgu_spl[0]+'/_/'+'/'.join(fgu_spl[1].split('/')[:2])

    r = requests.get(full_gallery_url)
    html = unicode(r.text)
    soup = BeautifulSoup(html)

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
    foldername="_temp"
    while os.path.exists('./'+foldername):
        foldername=foldername+str(randint(0,9))
    os.makedirs('./'+foldername)

    errors = 0
    for i in range(len(pages)):
        p = pages[i]
        
        logger.info("Downloading "+str(i+1)+"/"+str(len(pages)))
        if guiprintfcn is not None:
            guiprintfcn("Downloading "+str(i+1)+"/"+str(len(pages)))
            
        page_url = full_gallery_url+'/'+str(p)
        r = requests.get(page_url)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        
        img_url = soup.body.find('img', attrs={'id':'comic_page'}).get('src')
        logger.info(img_url)
        
        if i<10:
            num = '000'+str(i)
        elif i<100:
            num = '00'+str(i)
        elif i<1000:
            num = '0'+str(i)
        else:
            num = str(i)
        
        img_filename = num+'.'+img_url.split('.')[-1]
        img_path = './'+foldername+'/'+img_filename
        
        try:
            download(img_url, img_path)
        except:
            logger.warning('BAD download for: '+img_url)
            errors+=1
        else:
            logger.info('OK download')

    logger.info("Download finished, Failed downloads = "+str(errors))

    archive_name = (ch_name+'_['+grp_name+'].zip').replace('/','-')
    logger.info('Compressing to: '+str(archive_name))
    zipf = zipfile.ZipFile(archive_name, 'w')
    zipdir('./'+foldername, zipf)
    zipf.close()

    shutil.rmtree('./'+foldername)
    
    return errors, archive_name

if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    full_gallery_url = raw_input("Enter url of galery you want to download:\n")
    getChapter(full_gallery_url)
    raw_input("Finished, press enter")
