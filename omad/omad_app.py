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

import sys, os, argparse

from PyQt4.QtGui import QApplication

from .downloader_window import DownloaderWindow
from .download_controller import DownloadController

def nogui(args):
    #test if we have all needed args
    if args.url is None:
        print("--url option is needed in nogui mode!")
        sys.exit(2)
    if args.range is None and args.list is False:
        print("--range (or --list) option is needed in nogui mode!")
        sys.exit(2)

    dc = DownloadController()

    print("Setting DownloadController url...")
    if args.login is not None:
        r = dc.setSeriesUrl(args.url, args.login[0], args.login[1])
    else:
        r = dc.setSeriesUrl(args.url)
    if not r: print("Wrong url! Exiting..."); sys.exit(2)

    print("Downloading gallery info for: %s" % (args.url, ))
    chapter_list = dc.getChaptersList()

    # -l --list option, print chapters and exit
    if args.list:
        print("Printing list of chapters...")
        for i in range(len(chapter_list)):
            print("%i - %s" % (i, chapter_list[i][0]))
        print("Exiting...")
        sys.exit(0)

    # test -r --range option
    if args.range is None or len(args.range)!=2:
        print("Incorrect range argument, exiting...")
        sys.exit(2)

    if args.range[1]<0:
        args.range[1] = len(chapter_list)
    else:
        args.range[1] = args.range[1]+1

    try:
        c_range = chapter_list[args.range[0]:args.range[1]]
    except Exception as e:
        print("Bad range! %s" % (e,))
        print("Exiting...")
        sys.exit(2)

    if len(c_range)==0:
        print("Nothing to download, exiting...")
        sys.exit(0)

    # downloading
    print("Starting download of %i chapters..." % (len(c_range),))
    print("from: %s" % (c_range[0][0],))
    print("to: %s" % (c_range[-1][0],))

    dc.downloadChapterRange(args.range[0], args.range[1]-1)
    print("Download Finished!!!")

    # Print failed downloads
    print("\nChapters with failed downloads:")
    for i, r in enumerate(dc.results):
        if r is False:
            print(chapter_list[i+args.range[0]][0])

    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description='OMAD (Online MAnga downloader)'
    )
    parser.add_argument(
        '-u', '--url',
        default=None,
        help='Url of manga galllery')
    parser.add_argument(
        '--login',
        default=None,
        type=str, metavar='STR', nargs=2,
        help='tuple of "USERNAME PASSWORD" for logging in.')
    parser.add_argument(
        '-r', '--range',
        default=None,
        type=int, metavar='N', nargs='+',
        help='Range of chapters to download [0 -1]')
    parser.add_argument(
       '--nogui',
        action='store_true',
        help='Disable GUI')
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Debug mode')
    parser.add_argument(
        '--logfile',
        action='store_true',
        help='Save log to file')
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List chapters and exit. Used for finding download range')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.logfile:
        try:
            os.remove("omad.log")
        except OSError:
            pass
        fh = logging.FileHandler("omad.log")
        fh.setFormatter(logging.Formatter(fmt='%(levelname)s:%(name)s:%(message)s'))
        logger.addHandler(fh)

    if args.nogui:
        nogui(args)
    else:
        app = QApplication(sys.argv)
        dw = DownloaderWindow()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
