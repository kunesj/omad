#!/usr/bin/env python3
# encoding: utf-8

import unittest
from nose.plugins.attrib import attr

from omad.download_controller import DownloadController

from omad.mangafox_model import MangafoxModel

class ModelsTest(unittest.TestCase):
    # if error, always first check if urls are not bad
    # testchapters should have special non-ASCII characters in their names

    # mangafox shows all manga as licensed when viewed from USA
    # needs to be korean/chinese comix to work on Travis
    mangafox_series_url = 'http://fanfox.net/manga/0_0_mhz/'
    mangafox_chapter_index = 0

    @attr(site='mangafox')
    def mangafox_test(self):
        dc = DownloadController()

        # test chapter list request
        mod = MangafoxModel(self.mangafox_series_url, dc.guiInfoFcn)
        chapters = mod.getChaptersList()

        # test chapter download
        r = mod.downloadChapter(chapters[self.mangafox_chapter_index], './')

        # test if download was sucessfull
        self.assertTrue(r)

    @attr(site='mangafox')
    def mangafox_test_bad_url(self):
        dc = DownloadController()

        # test chapter request exception
        mod = MangafoxModel("http://fanfox.net", dc.guiInfoFcn)
        r = mod.downloadChapter(["bad_chapter", "http://mangafox.me/manga/asdfgh"], './')

        self.assertFalse(r)

