#!/usr/bin/python2
# coding: utf-8
"""
This file is part of Manga Downloader.

Manga Downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

Manga Downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Manga Downloader.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
logger = logging.getLogger(__name__)

import sys

from PyQt4.QtGui import QApplication

from downloader_window import DownloaderWindow

def main():
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    app = QApplication(sys.argv)
    dw = DownloaderWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
