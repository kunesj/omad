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

import sys

from omad.archive_controller import ArchiveController
from omad.misctools.fixed_requests import FixedRequests

class SiteModel(object):
    def __init__(self, series_url, gui_info_fcn):
        # init variables
        self.guiInfoFcn = None
        self.series_url = None
        self.requests = FixedRequests()

        # set variables
        self.setGuiInfoFcn(gui_info_fcn)
        self.setSeriesUrl(series_url)

    def setGuiInfoFcn(self, gui_info_fcn):
        self.guiInfoFcn = gui_info_fcn

    def setSeriesUrl(self, series_url):
        self.series_url = series_url

    def login(self, username, password):
        """
        Should be reimplemented by child class (if login is required).

        Returns True if OK, False if failed.
        """
        return self.getLogin()

    def getLogin(self):
        """
        Should be reimplemented by child class (if login is required).
        Returns True if user is logged in
        """
        return False

    def getChaptersList(self):
        """
        Needs to be reimplemented!

        Returns:
            [[chapter_name, url], [chapter_name, url], ...]
        """
        return []

    def getGalleryInfo(self, chapter):
        """
        Needs to be reimplemented!

        Items in page_urls can be image urls, if all images in chapter were on one webpage.

        Input:
            chapter = [chapter_name, url]

        Returns:
            [chapter_name, group_name, page_urls=[]]
        """
        return ['NOT-IMPLEMENTED', '', []]

    def getImageUrl(self, page_url):
        """
        Needs to be reimplemented!

        page_url can be actually image_url, if all images in chapter were on one webpage.

        Input:
            page_url

        Returns:
            [image_url, image_extension]
        """
        return None

    def downloadChapter(self, chapter, download_path):
        """
        Will download and compress chapter

        Input:
            chapter = [chapter_name, url]
            download_path = where to put compressed chapter
        """
        # get gallery info and url to every page
        try:
            gallery_info = self.getGalleryInfo(chapter)
        except Exception as e:
            logger.debug('Failed to get gallery info for chapter: '+str(chapter))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            self.guiInfoFcn(e, exception=True, trace=trace)
            return False

        ch_name = gallery_info[0]
        grp_name = gallery_info[1]
        pages = gallery_info[2]
        gallery_size = len(pages)

        logger.info('Downloading: '+ch_name)
        logger.info('Url: '+chapter[1])
        logger.info('Pages: '+str(gallery_size))

        # create temp folder for downloads
        ac = ArchiveController(download_path)
        ac.set_requests_object(self.requests)
        ac.mkdir()

        for i in range(gallery_size):
            self.guiInfoFcn("Downloading page "+str(i+1)+"/"+str(gallery_size))

            # get image url
            img = self.getImageUrl(pages[i])
            img_url = img[0]; img_ext = img[1]
            logger.info(img_url)

            # create image filename
            num = str(i).zfill(4)
            img_filename = num+'.'+img_ext

            # download image to temp folder
            try:
                ac.download(img_url, img_filename)
            except Exception as e:
                logger.exception('BAD download for: '+img_url)
                self.guiInfoFcn("Error downloading page image")
                return False
            else:
                logger.debug('OK download')

        logger.info("Download finished without any errors")

        # create archive filename
        if grp_name != '':
            grp_name = ' ['+grp_name+']'
        archive_name = ac.sanitize_filename(ch_name+grp_name+'.zip')

        # compress temp folder to archive
        self.guiInfoFcn('Compressing to: '+archive_name)
        ac.zipdir(archive_name)

        # remove temp folder
        ac.rmdir()

        return True
