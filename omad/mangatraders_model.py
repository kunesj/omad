#!/usr/bin/env python3
# encoding: utf-8
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

from bs4 import BeautifulSoup

from omad.sitemodel import SiteModel

class MangatradersModel(SiteModel):

    def __init__(self, series_url, gui_info_fcn):
        super(MangatradersModel, self).__init__(series_url, gui_info_fcn)

    def setSeriesUrl(self, series_url):
        # default to chapter reading view
        if 'mangatraders.biz/series/' in series_url:
            self.guiInfoFcn("Mangatraders url is series url, trying to get manga url... ")

            # get base series name
            base_name = series_url.split('mangatraders.biz/series/')[-1]

            # add '-' between words
            newurl = 'http://mangatraders.biz/manga/'
            for i, c in enumerate(base_name):
                if c.isupper() and i!=0:
                    newurl += '-'+c
                else:
                    newurl += c

            # test new series url
            try:
                self.requests.get(url=newurl)
            except Exception:
                raise Exception("Failed getting Mangatraders manga url! Please login in browser and use chapter list url!")
            else:
                self.guiInfoFcn("Got Mangatraders manga url '%s'" % newurl)

            self.series_url = newurl
        else:
            self.series_url = series_url

    def getChaptersList(self):
        """
        Returns:
            [[chapter_name, url], [chapter_name, url], ...]
        """
        r = self.requests.get(url=self.series_url)
        soup = BeautifulSoup(r.text, 'lxml')

        div_chapterlist = soup.find('div', attrs={'class':'list chapter-list'})

        processed_chapters = []
        for a in div_chapterlist.findAll('a'):
            name = a.span.text.strip()
            href = a.get('href')
            if not 'mangatraders.biz' in href:
                href = 'http://mangatraders.biz'+href
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
        cut_gallery_url = '-page-'.join(full_gallery_url.split('-page-')[:-1])

        # download html
        r = self.requests.get(url=full_gallery_url)
        soup = BeautifulSoup(r.text, 'lxml')

        # parse html
        div_row = soup.body.find('div', attrs={'class':'mainWrapper'}).find('div', attrs={'class':'row'})

        series_name = div_row.find('input', attrs={'class':'SeriesName'}).get('value')
        ch_number = div_row.find('span', attrs={'class':'CurChapter'}).text.strip()
        ch_name = series_name+' - Chapter '+ch_number
        grp_name = ''

        # get page_urls
        select_pages = div_row.findAll('select')[1]
        pages = []
        for o in select_pages.findAll('option'):
            pages.append("%s-page-%s.html" % (cut_gallery_url, o.get('value')) )

        return [ch_name, grp_name, pages]

    def getImageUrl(self, page_url):
        """
        Input:
            page_url

        Returns:
            [image_url, image_extension]
        """
        r = self.requests.get(url=page_url)
        soup = BeautifulSoup(r.text, 'lxml')

        img_url = soup.find('img', attrs={'class':'CurImage'}).get('src')
        img_ext = img_url.split('.')[-1]

        return  [img_url, img_ext]

if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    from download_controller import DownloadController
    dc = DownloadController()

    mod = MangatradersModel("http://mangatraders.biz/series/MahouTsukaiNoYome", dc.guiInfoFcn)
    chapters = mod.getChaptersList()
    print(chapters[0])
    print(mod.downloadChapter(chapters[0], './'))
