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

import requests
from bs4 import BeautifulSoup

import batoto_chapter_downloader

def getListOfChapters(url):
    r = requests.get(url)
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
    
if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    
    full_series_url = raw_input("Enter url of series download:\n")
    processed_chapters = getListOfChapters(full_series_url)
        
    print 'Found '+str(len(processed_chapters))+' english chapters'
    print 'First [0]: '+processed_chapters[0][0]
    print 'Last ['+str(len(processed_chapters)-1)+']: '+processed_chapters[-1][0]

    ok = False
    while not ok:
        start = raw_input("From which chapter start download [list pos] (default 0):\n")
        if start.isdigit():
            start = int(start)
            if start>len(processed_chapters)-1:
                print 'Wrong number defaulting to 0'
                start = 0
        else:
            print 'Not number defaulting to 0'
            start = 0

        end = raw_input("At which chapter end download [list pos] (default max):\n")
        if end.isdigit():
            end = int(start)
            if end>len(processed_chapters)-1 or start>end:
                print 'Wrong number defaulting to '+str(len(processed_chapters)-1)
                end = len(processed_chapters)-1
        else:
            print 'Not number defaulting to '+str(len(processed_chapters)-1)
            end = len(processed_chapters)-1

        # ASK IF RANGE IS OKAY
        print 'Will download chapters, '
        print 'from: '+processed_chapters[start][0]
        print 'to: '+processed_chapters[end][0]
        resp = raw_input("Correct range? (y/n)")
        if resp.lower() == 'y' or resp.lower() == 'yes':
            ok = True

    filtered_chs = processed_chapters[start:end+1]

    # Download chapters
    failed_ch = []
    for ch in filtered_chs:
        print 'Downloading: '+ch[0]
        
        err, name = batoto_chapter_downloader.getChapter(ch[1])
        if err!=0:
            print 'Download finished with errors'
            failed_ch.append(ch)
        
        print 'Saved: '+name
            
    print 'Chapters with failed downloads:'
    for f in failed_ch:
        print f[0]

    raw_input("Finished, press enter")

