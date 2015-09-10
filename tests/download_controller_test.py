#!/usr/bin/python2
# coding: utf-8

import os, sys

import unittest
from nose.plugins.attrib import attr

from omad.download_controller import DownloadController

from omad.mangafox_model import MangafoxModel
from omad.batoto_model import BatotoModel
from omad.kissmanga_model import KissmangaModel
from omad.mangatraders_model import MangatradersModel

class DownloadControllerTest(unittest.TestCase):
    # allways test urls first
    mangafox_series_url = 'http://mangafox.me/manga/ai_yori_aoshi/'
    batoto_series_url = 'http://bato.to/comic/_/comics/fatekaleid-liner-prisma%E2%98%86illya-3rei-r7635'
    kissmanga_series_url = 'http://kissmanga.com/Manga/Fate-Kaleid-Liner-Prisma-Illya-Drei' 
    mangatraders_series_url = 'http://mangatraders.org/manga/?series=FateKaleidLinerPrismaIllyaDrei&uploader=Ravmunken' 
    
    def select_url_bad_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl("http://www.google.com")
        
        self.assertFalse(r)
        self.assertTrue( dc.webpage_model is None )
    
    def select_url_mangafox_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl(self.mangafox_series_url)
        
        self.assertTrue(r)
        self.assertTrue( isinstance(dc.webpage_model, MangafoxModel) )
    
    def select_url_batoto_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl(self.batoto_series_url)
        
        self.assertTrue(r)
        self.assertTrue( isinstance(dc.webpage_model, BatotoModel) )
        
    def select_url_kissmanga_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl(self.kissmanga_series_url)
        
        self.assertTrue(r)
        self.assertTrue( isinstance(dc.webpage_model, KissmangaModel) )
        
    def select_url_mangatraders_test(self):
        dc = DownloadController()
        r = dc.setSeriesUrl(self.mangatraders_series_url)
        
        self.assertTrue(r)
        self.assertTrue( isinstance(dc.webpage_model, MangatradersModel) )
    
    def download_path_test(self):
        dpath = "./"
        dc = DownloadController()
        dc.setDownloadPath(dpath)
        r = dc.getDownloadPath()
        
        self.assertEqual(os.path.abspath(dpath), os.path.abspath(r))
    
    def download_range_test(self):
        dc = DownloadController()
        dc.setSeriesUrl(self.kissmanga_series_url)
        r = dc.downloadChapterRange(0, 1)
        
        self.assertFalse(False in r)
