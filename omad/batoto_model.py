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
import traceback

from omad.sitemodel import SiteModel

from bs4 import BeautifulSoup

class BatotoModel(SiteModel):
    def __init__(self, series_url, gui_info_fcn):
        super(BatotoModel, self).__init__(series_url, gui_info_fcn)
        self.requests.updateHeaders({'referer': 'https://bato.to/reader'})

    def getChaptersList(self):
        """
        Returns:
            [[chapter_name, url], [chapter_name, url], ...]
        """
        r = self.requests.get(url=self.series_url)
        soup = BeautifulSoup(r.text, 'lxml')

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

    def getGalleryInfo(self, chapter):
        """
        Input:
            chapter = [chapter_name, url]

        Returns:
            [chapter_name, group_name, page_urls=[]]
        """

        # get url
        full_gallery_url = chapter[1]
        if full_gallery_url.endswith('/'):
            full_gallery_url = full_gallery_url[:-1]

        gallery_id = full_gallery_url.split('reader#')[-1].split('_')[0]
        reader_page_url = "https://bato.to/areader?id="+gallery_id+"&p=1&supress_webtoon=t"

        # get html
        r = self.requests.get(url=reader_page_url)
        soup = BeautifulSoup(r.text, 'lxml')

        # parse html
        div_modbar = soup.find('div', attrs={'class':'moderation_bar rounded clear'})
        series_name = div_modbar.find('a').text.replace('/',' ')
        ch_select = div_modbar.find('select', attrs={'name':'chapter_select'})
        ch_name = series_name+' - '+ch_select.find('option', attrs={'selected':'selected'}).text.strip()

        grp_select = div_modbar.find('select', attrs={'name':'group_select'})
        grp_name = grp_select.find('option', attrs={'selected':'selected'}).text
        # remove language from group
        grp_name = '-'.join(grp_name.split('-')[:-1]).strip()

        # get page_urls
        pages = div_modbar.find('select', attrs={'name':'page_select'}).text.lower().split('page')[1:]
        pages = [x.strip() for x in pages]

        page_urls = []
        for p in pages:
            page_urls.append( "https://bato.to/areader?id="+gallery_id+"&p="+str(p)+"&supress_webtoon=t" )


        return [ch_name, grp_name, page_urls]

    def getImageUrl(self, page_url):
        """
        Input:
            page_url

        Returns:
            [image_url, image_extension]
        """
        r = self.requests.get(url=page_url)
        soup = BeautifulSoup(r.text, 'lxml')

        img_url = soup.find('img', attrs={'id':'comic_page'}).get('src')
        img_ext = img_url.split('.')[-1]

        return [img_url, img_ext]
