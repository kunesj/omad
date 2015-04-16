Manga Downloader
=================

Simple application for downloading chapters from online manga reading sites.

![ScreenShot](https://raw.github.com/kunesj/manga_downloader/master/doc/manga-downloader.png)

Supported sites:

    bato.to
    kissmanga.com
    mangafox.me

Optional commandline parameters:

      -h, --help            show this help message and exit
      -u URL, --url URL     Url of manga galllery
      -r N [N ...], --range N [N ...]
                            Range of chapters to download [0 -1]
      --nogui               Disable GUI
      -d, --debug           Debug mode
      -l, --list            List chapters and exit. Used for finding download
                            range



Install on Linux (Debian/Ubuntu/Mint)
-------
Get zipped source and extract it anywhere you want:

    https://github.com/kunesj/manga_downloader

Install required dependencies:

    sudo apt-get install python python-pip python-qt4 
    sudo pip install requests beautifulsoup4

Install on Windows
-------
Get zipped source and extract it anywhere you want:

    https://github.com/kunesj/manga_downloader
    
Install Python 2, setupTools, pip and PyQt4:

- [Python 2.x](https://www.python.org/downloads/windows/)
- [Python 2.x - setupTools](http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools)
- [Python 2.x - pip](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip)
- [Python 2.x - PyQt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt)
    
Run from command line to install rest of dependencies:
    
    C:\Python27\Scripts\pip.exe install requests beautifulsoup4
    
