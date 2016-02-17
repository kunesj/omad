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

from sitemodel import SiteModel

import requests
import urlparse
try:
    from BeautifulSoup import BeautifulSoup
except:
    # windows fix
    from bs4 import BeautifulSoup 

class MangatradersModel(SiteModel):
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
        super(MangatradersModel, self).__init__(series_url, gui_info_fcn)
    
    def setSeriesUrl(self, series_url):
        # fix url
        params = urlparse.parse_qs(urlparse.urlparse(series_url).query)
        if 'series' in params:
            series_url = 'http://mangatraders.org/read-online/'+params['series'][0]
            logger.info('Series url autochanged to: '+series_url)
        self.series_url = series_url

    def getChaptersList(self):
        """
        Returns:
            [[chapter_name, url], [chapter_name, url], ...]
        """
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

    def getGalleryInfo(self, chapter):
        """
        Input:
            chapter = [chapter_name, url]

        Returns:
            [chapter_name, group_name, page_urls=[]]
        """
        
        # get url
        full_gallery_url = chapter[1]
        cut_gallery_url = full_gallery_url.split('/page-')[0]
        
        # download html
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
        
        # get page_urls
        pages = []
        pages_options = mainPageContainer.find('ol') \
            .find('select', attrs={'id':'changePageSelect'}).findAll('option')
        for p in pages_options:
            pages.append(cut_gallery_url+'/'+p.get('value'))
        
        return [ch_name, grp_name, pages]

    def getImageUrl(self, page_url):
        """
        Input:
            page_url

        Returns:
            [image_url, image_extension]
        """
        r = requests.get(page_url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        
        img_url = soup.body \
            .find('div', attrs={'style':'text-align:center;'}) \
            .find('img').get('src')
        img_ext = img_url.split('.')[-1].split('?')[0]
        
        return  [img_url, img_ext]
