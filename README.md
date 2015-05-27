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
There are 3 ways you can do this.

1. Static binary way (Doesnt need root or any installed dependencies)
    - Download archived binary file from latest [release](https://github.com/kunesj/omad/releases).
    - Extract "omad" file to any folder in your system path (best places are ~/bin or /usr/local/bin).
    - Extract omad.desktop to ~/.local/share/application or /usr/local/share/applications
    - You can now start OMAD with shortcut from global menu or from commandline with "omad" command

2. Package install way (Proper Python way)
    - Download archived source from latest [release](https://github.com/kunesj/omad/releases).
    - Extract it anywhere you want
    - In terminal in folder with extracted files, run: "make install"
    - Remove folder with extracted source
    - You can now start OMAD with shortcut from global menu or from commandline with "omad" command

3. Source only way (For developers)
    - Download archived source from latest [release](https://github.com/kunesj/omad/releases).
    - Extract it anywhere you want
    - In terminal in folder with extracted files, run: "make install_dep" to install runtime dependencies
    - You can only start OMAD from commandline, by directly using Python interpreter (python -m omad)

Install on Windows
-------
!WINDOWS IS NOT TESTED/SUPPORTED!

Get zipped source and extract it anywhere you want:

    https://github.com/kunesj/omad
    
Install Python 2, setupTools, pip and PyQt4: (everything must be for Python 2)

- [Python 2.x](https://www.python.org/downloads/windows/)
- [Python 2.x - setupTools](http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools)
- [Python 2.x - pip](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip)
- [Python 2.x - PyQt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt)
    
Run from command line to install rest of dependencies:
    
    C:\Python27\Scripts\pip.exe install requests beautifulsoup4
    
You can only start OMAD from commandline, by directly using Python interpreter (python -m omad)
    
