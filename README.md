OMAD
====

OMAD (Online MAnga Downloader) is a simple application for downloading chapters from online manga reading sites.

![ScreenShot](https://raw.github.com/kunesj/omad/master/doc/preview.png)

Supported sites:

    bato.to
    kissmanga.com
    mangafox.me
    mangatraders.org

Optional commandline parameters:

      -h, --help            show this help message and exit
      -u URL, --url URL     Url of manga galllery
      -r N [N ...], --range N [N ...]
                            Range of chapters to download [0 -1]
      --nogui               Disable GUI
      -d, --debug           Debug mode
      --logfile             Save log to file
      -l, --list            List chapters and exit. Used for finding download
                            range



Install on Linux (Debian/Ubuntu/Mint)
-------
Get zipped source and extract it anywhere you want:

    https://github.com/kunesj/omad

To install both required dependencies and application to local system run from source directory:

    make install
    
Its now possible to Launch application directly from command line with:

    omad

If you want to uninstall, you can do it by running:

    make uninstall

Optionally you can only install dependencies and run application directly from downloaded source:

    make install_dep

Install on Windows
-------
Get zipped source and extract it anywhere you want:

    https://github.com/kunesj/omad
    
Install Python 2, setupTools, pip and PyQt4:

- [Python 2.x](https://www.python.org/downloads/windows/)
- [Python 2.x - setupTools](http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools)
- [Python 2.x - pip](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip)
- [Python 2.x - PyQt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt)
    
Run from command line to install rest of dependencies:
    
    C:\Python27\Scripts\pip.exe install requests beautifulsoup4
    
