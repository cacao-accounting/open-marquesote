# Copyright 2017 Martin Fitzpatrick
# Copyright 2020 William Moreno Reyes
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from PyQt5.QtCore import (
    QSize,
    QUrl,
)
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QMainWindow,
    QStatusBar,
    QTabWidget,
    QToolBar,
)
from PyQt5.QtGui import (
    QIcon,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import QPrintPreviewDialog

import os
import sys


home = os.path.abspath(os.path.dirname(__file__))


class MainWindow(QMainWindow):
    def __init__(self, url=None, appname=None, *args, **kwargs):
        if url:
            self.url = url
        else:
            self.url = "https://github.com/cacao-accounting/cacao-accounting"
        if appname:
            self.appname = appname
        else:
            self.appname = "Open Marquesote"
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join(home, "images", "back.png")), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join(home, "images", "next.png")), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join(home, "images", "reload.png")), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join(home, "images", "home.png")), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        # print_action = QAction(QIcon(os.path.join(home, "images", "printer.png")), "Print...", self)
        # print_action.setStatusTip("Print current page")
        # print_action.triggered.connect(self.print_page)
        # navtb.addAction(print_action)
        new_tab_action = QAction(QIcon(os.path.join(home, "images", "ui-tab--plus.png")), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        navtb.addAction(new_tab_action)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        self.add_new_tab(QUrl(self.url), self.appname)

        self.show()

        if self.appname is None:
            self.setWindowTitle(self.appname)
        else:
            self.setWindowTitle(self.appname)
        self.setWindowIcon(QIcon(os.path.join(home, "images", "ma-icon-64.png")))

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl(self.url)

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)

    def print_page(self):
        dlg = QPrintPreviewDialog()
        #dlg.paintRequested.connect()
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(self.url))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.url)
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
