#!/usr/bin/env python3
# encoding: utf-8

import unittest
from nose.plugins.attrib import attr

import os, sys

from omad.omad_app import main, nogui

class OMADAppTest(unittest.TestCase):
    """
    Can only test if return codes
    """
    series_url = 'http://mangafox.me/manga/0_0_mhz/'
    chapter_index = 0

    def main_nogui_bad_args_test(self):
        print("--------------")
        sys.argv = [ sys.argv[0], '--nogui']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # missing --url

        print("--------------")
        sys.argv = [ sys.argv[0], '--nogui', '--url', self.series_url ]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # missing --list or --range

        print("--------------")
        sys.argv = [ sys.argv[0], '--nogui', '--url', 'asdf', '--list' ]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # bad url

        print("--------------")
        sys.argv = [ sys.argv[0], '--nogui', '--url', self.series_url, '--range', '0', '1', '2' ]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # too many range arguments

    def main_nogui_list_test(self):
        sys.argv = [ sys.argv[0], '--nogui', '--url', self.series_url, '--list']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)

    def main_logfile_test(self):
        sys.argv = [ sys.argv[0], '--nogui', '--logfile', '--debug']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)

    def main_nogui_download_test(self):
        sys.argv = [ sys.argv[0], '--nogui', '--url', self.series_url, '--range', '0', '0']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
