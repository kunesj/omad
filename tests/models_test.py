#!/usr/bin/python2
# coding: utf-8

import unittest
from nose.plugins.attrib import attr

from omad.download_controller import DownloadController

from omad.mangafox_model import MangafoxModel
from omad.batoto_model import BatotoModel
from omad.mangatraders_model import MangatradersModel

class ModelsTest(unittest.TestCase):
    # if error, always first check if urls are not bad
    # testchapters should have special non-ASCII characters in their names
    
    # mangafox shows all manga as licensed when viewed from USA
    mangafox_series_url = 'http://mangafox.me/manga/0_0_mhz/' # needs to be korean/chinese comix to work on Travis
    mangafox_chapter_index = 0

    batoto_series_url = 'http://bato.to/comic/_/comics/fatekaleid-liner-prisma%E2%98%86illya-3rei-r7635' # special char in series name
    batoto_chapter_index = 0 # http://bato.to/read/_/145348/fatekaleid-liner-prisma%E2%98%86illya-3rei_ch1_by_suimasen-scans

    mangatraders_series_url = 'http://mangatraders.org/manga/?series=FateKaleidLinerPrismaIllyaDrei&uploader=Ravmunken' # slash in series name
    mangatraders_chapter_index = 0 #


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
        mod = MangafoxModel("http://mangafox.me", dc.guiInfoFcn)
        r = mod.downloadChapter(["bad_chapter", "http://mangafox.me/manga/asdfgh"], './')

        self.assertFalse(r)

    @attr(site='batoto')
    def batoto_test(self):
        dc = DownloadController()

        # test chapter list request
        mod = BatotoModel(self.batoto_series_url, dc.guiInfoFcn)
        chapters = mod.getChaptersList()

        # test chapter download
        r = mod.downloadChapter(chapters[self.batoto_chapter_index], './')

        # test if download was sucessfull
        self.assertTrue(r)

    @attr(site='batoto')
    def batoto_test_bad_url(self):
        dc = DownloadController()

        # test chapter request exception
        mod = BatotoModel("http://bato.to", dc.guiInfoFcn)
        r = mod.downloadChapter(["bad_chapter", "http://bato.to/comic/_/comics/asdfgh"], './')

        self.assertFalse(r)

    @attr(site='mangatraders')
    def mangatraders_test(self):
        dc = DownloadController()

        # test chapter list request
        mod = MangatradersModel(self.mangatraders_series_url, dc.guiInfoFcn)
        chapters = mod.getChaptersList()

        # test chapter download
        r = mod.downloadChapter(chapters[self.mangatraders_chapter_index], './')

        # test if download was sucessfull
        self.assertTrue(r)

    @attr(site='mangatraders')
    def mangatraders_test_bad_url(self):
        dc = DownloadController()

        # test chapter request exception
        mod = MangatradersModel("http://mangatraders.org", dc.guiInfoFcn)
        r = mod.downloadChapter(["bad_chapter", "http://mangatraders.org/manga/asdfgh"], './')

        self.assertFalse(r)
