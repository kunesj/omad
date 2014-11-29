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

from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,\
                        QTextEdit, QLineEdit, QLabel, QComboBox, QPushButton,\
                        QTextCursor, QApplication

from download_controller import DownloadController

class DownloaderWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.down_control = DownloadController(self.addInfo)
        
        self.chapters = None
        self.chapters_filtered = None
 
        self.resize(700, 400)
        self.initUI()   
             
    def initUI(self):
        cw = QWidget()
        self.setCentralWidget(cw)
        layout_main = QVBoxLayout()
        layout_main.setSpacing(5)
        
        ## Info
        self.info = QTextEdit()
        self.info.setReadOnly(True)
        self.info.setLineWrapMode(QTextEdit.NoWrap)
        
        layout_main.addWidget(self.info, 1)
        
        ## Line edit
        layout_url = QHBoxLayout()
        layout_url.setSpacing(5)
        
        self.line_url = QLineEdit()
        
        layout_url.addWidget(QLabel('Series URL:'))
        layout_url.addWidget(self.line_url, 1)
        layout_main.addLayout(layout_url)
        
        ## Comboboxes
        layout_combo = QHBoxLayout()
        layout_combo.setSpacing(5)
        
        self.combo_from = QComboBox()
        self.combo_from.setEnabled(False)
        self.combo_to = QComboBox()
        self.combo_to.setEnabled(False)
        
        layout_combo.addWidget(QLabel('<b>Download chapters: </b>'))
        layout_combo.addWidget(QLabel(' From:'))
        layout_combo.addWidget(self.combo_from, 1)
        layout_combo.addWidget(QLabel('To:'))
        layout_combo.addWidget(self.combo_to, 1)
        
        layout_main.addLayout(layout_combo)
        
        ## Buttons
        layout_btn = QHBoxLayout()
        layout_btn.setSpacing(5)
        
        self.btn_getlist = QPushButton('Get List of Chapters')
        self.btn_getlist.pressed.connect(self.getChaptersList)
        self.btn_download = QPushButton('Download chapters')
        self.btn_download.pressed.connect(self.downloadChapters)
        self.btn_download.setEnabled(False)
        self.btn_exit = QPushButton('Exit')
        self.btn_exit.pressed.connect(self.close)
        
        layout_btn.addStretch()
        layout_btn.addWidget(self.btn_getlist)
        layout_btn.addWidget(self.btn_download)
        layout_btn.addWidget(self.btn_exit)
        layout_btn.addStretch()
        layout_main.addLayout(layout_btn)
        
        # add layout to main window
        cw.setLayout(layout_main)
        self.setWindowTitle('Manga Downloader')
        self.show()
        
    def addInfo(self, s='Testing printing...'):
        s+='\n'
        self.info.moveCursor(QTextCursor.End)
        self.info.insertPlainText(s)
        
        sb = self.info.verticalScrollBar()
        sb.setValue(sb.maximum())
        
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.processEvents()
        
    def getChaptersList(self):
        self.addInfo('Getting list of chapters...')
        
        url = str(self.line_url.text()).strip()
        
        if not self.down_control.setSeriesUrl(url):
            return # bad url
            
        self.chapters = self.down_control.getChaptersList()
        
        for c in self.chapters:
            self.combo_from.addItem(c[0])
            self.combo_to.addItem(c[0])
            
        self.combo_from.setCurrentIndex(0)
        self.combo_to.setCurrentIndex(len(self.chapters)-1)
            
        self.addInfo('Chapter list loaded')
        
        self.combo_from.setEnabled(True)
        self.combo_to.setEnabled(True)
        self.btn_download.setEnabled(True)
        
    def downloadChapters(self):
        self.addInfo('Checking chapter range')
        
        ch_from = self.combo_from.currentIndex()
        ch_to = self.combo_to.currentIndex()
        
        if ch_from>ch_to:
            self.addInfo('Bad range. Cant download backwards!')
            return
        else:
            self.addInfo('Range OK, starting download of '+str((ch_to-ch_from)+1)+' chapters...')
            
        results = self.down_control.downloadChapterRange(ch_from, ch_to)
        
        # Finished        
        self.addInfo('Download Finished!!!')
        
        # Print failed downloads
        self.addInfo('\nChapters with failed downloads:')  
        for i, r in enumerate(results):
            if r is False:
                self.addInfo(self.chapters[i+ch_from][0])
