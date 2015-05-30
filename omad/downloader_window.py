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
import sys
import os

from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal, QObject, QRunnable, QThreadPool, Qt
from PyQt4.QtGui import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,\
                        QTextEdit, QLineEdit, QLabel, QComboBox, QPushButton, \
                        QFileDialog

from download_controller import DownloadController

class DownloadWorker(QRunnable):
    class DownloadWorkerSignals(QObject):
        update = pyqtSignal(str,bool,bool,list)
        finished = pyqtSignal()
    
    def __init__(self, downloadController, ch_from, ch_to):
        super(DownloadWorker, self).__init__()
        self.downloadController = downloadController
        self.ch_from = ch_from
        self.ch_to = ch_to
        
        self.signals = self.DownloadWorkerSignals()
    
    def run(self):
        try:
            self.downloadController.setGuiInfoFcn(self.signals.update.emit)
            self.downloadController.downloadChapterRange(self.ch_from, self.ch_to)
        except Exception, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            self.downloadController.guiInfoFcn(e, exception=True, trace=trace)
        self.signals.finished.emit()

class DownloaderWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.DownloadPath = os.path.expanduser("~") # get home dir
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(1)
        
        self.initVariables()
 
        self.resize(700, 400)
        self.initUI()   
        
        self.line_downpath.setText(self.down_control.getDownloadPath())
        
    def initVariables(self):
        self.down_control = DownloadController(self.addInfo)
        self.down_control.setDownloadPath(self.DownloadPath)
        self.chapters = None
        self.chapters_filtered = None
        self.ch_from = None
        self.ch_to = None
             
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
        
        layout_url.addWidget(QLabel('<b>Series URL:</b>'))
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
        
        ## Download path
        layout_downpath = QHBoxLayout()
        layout_downpath.setSpacing(5)
        
        self.line_downpath = QLineEdit()
        self.line_downpath.setEnabled(False)
        self.btn_downpath = QPushButton('Change')
        self.btn_downpath.pressed.connect(self.selectDownloadPath)
        
        layout_downpath.addWidget(QLabel('<b>Download path:</b>'))
        layout_downpath.addWidget(self.line_downpath, 1)
        layout_downpath.addWidget(self.btn_downpath)
        layout_main.addLayout(layout_downpath)
        
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
        
        # status bar
        self.statusBar().showMessage('Ready')
        
        # add layout to main window
        cw.setLayout(layout_main)
        self.setWindowTitle('OMAD - Online MAnga Downloader')
        self.show()
        
    def closeEvent(self, event):
        """
        Runs when user tryes to close main window.

        sys.exit(0) - to fix wierd bug, where process is not terminated.
        """
        sys.exit(0)
        
    def addInfo(self, s='Testing printing...', exception=False, downloadProgress=False, trace=[]):
        logger.info(s+', '+str(exception)+', '+str(downloadProgress)+', '+str(trace))
        
        if not isinstance(s, basestring) and type(s) != type(QtCore.QString('')):
            s = str(s)
        
        if exception:
            s = "!!! Exception: "+s
        
        if downloadProgress:
            s = "Downloading progress: "+s
            self.setStatusBarText(s)
        
        self.info.append(s)
        
        if exception:
            for t in trace:
                self.info.append(str(t))
        
        sb = self.info.verticalScrollBar()
        sb.setValue(sb.maximum())
        
        QtCore.QCoreApplication.processEvents()
        
    def setStatusBarText(self, s='Testing...'):
        """
        Changes status bar text
        """
        self.statusBar().showMessage(s)
        QtCore.QCoreApplication.processEvents()
    
    def getChaptersList(self):        
        self.addInfo('Getting list of chapters...')
        
        # reinit clean variables
        self.initVariables()
        
        # get series url
        url = str(self.line_url.text()).strip()
        
        if not self.down_control.setSeriesUrl(url):
            return # bad url
            
        self.chapters = self.down_control.getChaptersList()
        
        logger.debug('Setting up comboBoxes...')
        for i in xrange(0, self.combo_from.count()):
            self.combo_from.removeItem(0)
        for i in xrange(0, self.combo_to.count()):
            self.combo_to.removeItem(0)
        
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
        
        self.ch_from = self.combo_from.currentIndex()
        self.ch_to = self.combo_to.currentIndex()
        
        if self.ch_from>self.ch_to:
            self.addInfo('Bad range. Cant download backwards!')
            return
        else:
            self.addInfo('Range OK, starting download of '+str((self.ch_to-self.ch_from)+1)+' chapters...')
        
        self.gui_disable(True)
        
        worker = DownloadWorker(self.down_control, self.ch_from, self.ch_to)
        worker.signals.update.connect(self.addInfo)
        worker.signals.finished.connect(self.downloadChapters_finished)
        self.pool.start(worker)
    
    def downloadChapters_finished(self):
        self.gui_disable(False)
        self.setStatusBarText('Ready - Download Finished!!')
        
        # Finished        
        self.addInfo('Download Finished!!')
        
        # Print failed downloads
        failed_chs = []
        for i, r in enumerate(self.down_control.results):
            if r is False:
                failed_chs.append(self.chapters[i+self.ch_from])
        
        if len(failed_chs)==0:
            self.addInfo('\nNo failed downloads') 
        else:
            self.addInfo('\nChapters with failed downloads:')  
            for c in failed_chs:
                self.addInfo(c[0])
        self.addInfo('') 
                
    def selectDownloadPath(self):
        downdir = self._get_dir(directory=self.DownloadPath)
        self.down_control.setDownloadPath(downdir)
        self.DownloadPath = self.down_control.getDownloadPath()
        self.line_downpath.setText(self.DownloadPath)
        
    def _get_dir(self, directory=''):
        """
        Draw a dialog for directory selection.
        """

        downdir = QFileDialog.getExistingDirectory(
            caption='Select Folder',
            options=QFileDialog.ShowDirsOnly,
            directory=directory
        )

        if len(downdir) > 0:
            downdir = "%s" % (downdir)
            downdir = downdir.encode("utf8")
        else:
            downdir = directory

        return downdir
                
    def gui_disable(self, downloading=True):
        self.line_url.setEnabled(not downloading)
        self.combo_from.setEnabled(not downloading)
        self.combo_to.setEnabled(not downloading)
        self.btn_getlist.setEnabled(not downloading)
        self.btn_download.setEnabled(not downloading)
        self.btn_downpath.setEnabled(not downloading)
    
