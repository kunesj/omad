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

try:
    from BeautifulSoup import BeautifulSoup
except:
    # windows fix
    from bs4 import BeautifulSoup

class MangafoxModel(SiteModel):
    def __init__(self, series_url, gui_info_fcn):
        super(MangafoxModel, self).__init__(series_url, gui_info_fcn)

    def getChaptersList(self):
        """
        Returns:
            [[chapter_name, url], [chapter_name, url], ...]
        """
        r = self.requests.get(url=self.series_url)
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
            name = BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).text
            href = ch.find('a').get('href')
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
        cut_gallery_url = '/'.join(chapter[1].split('/')[:-1])+'/'+'1.html'

        # download html
        r = self.requests.get(url=cut_gallery_url)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        print html, r.request.headers, full_gallery_url, cut_gallery_url

        # parse html
        ch_name = chapter[0]
        grp_name = ''

        # get page_urls
        pages = []
        select = soup.body.find('select', attrs={'class':'m'})
        select_options = select.findAll('option')
        for o in select_options:
            try:
                int(o.text)
            except:
                continue
            pages.append(cut_gallery_url+o.text+'.html')

        return [ch_name, grp_name, pages]

    def getImageUrl(self, page_url):
        """
        Input:
            page_url

        Returns:
            [image_url, image_extension]
        """
        r = self.requests.get(url=page_url)
        html = unicode(r.text)
        soup = BeautifulSoup(html)

        img_url = soup.body.find('img', attrs={'id':'image'}).get('src')
        img_ext = img_url.split('.')[-1].split('?')[0]

        return [img_url, img_ext]
