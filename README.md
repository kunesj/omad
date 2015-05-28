OMAD
====

[![Join the chat at https://gitter.im/kunesj/omad](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/kunesj/omad?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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
You can download archived binary file from latest [release](https://github.com/kunesj/omad/releases) and just use that, or you can follow these instructions and install everything manualy. (When binary for some reason doesnt work)

1. Install Python 2
    - Download [Python 2.x](https://www.python.org/downloads/windows/) installer (includes pip and setuptools)
    - Run installer and select to add python to system path

2. Install PyQt4
    - Download [Python 2.x - PyQt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) wheels package
    - From commandline in folder with downloaded file run following command, you may need to modify it for correct filename: 

    pip install PyQt4-4.11.3-cp27-none-win32.whl

3. Install rest of runtime dependencies
    - From commandline run following command:

    pip install requests beautifulsoup4
    
4. Install OMAD
    - Get zipped [source](https://github.com/kunesj/omad/releases) and extract it anywhere you want
    - Run following commands from folder with extracted files, to finish installation:
    
    python setup.py build

    python setup.py install
    
    copy .\OMAD.lnk "%USERPROFILE%\Start Menu\Programs\"

    - You can now start OMAD with shortcut from startmenu or from commandline with "omad" command


Building static binary
------- 

1. Linux
    - In terminal in omad folder, run: "make build_dep" to install build dependencies
    - Then run: "make build" to build binary and package it together with source into tar archive
    
2. Windows
    - Follow installation instructions, until you install all dependencies
    - Download and install [pywin32](http://sourceforge.net/projects/pywin32) (make sure it's Python 2 version)
    - Download and install [MSVCR](https://www.microsoft.com/en-us/download/details.aspx?id=29)
    - Download and install [Git](https://git-scm.com/downloads), in installation select to use git from windows commandline
    - Download source of development version of [PyInstaller](https://github.com/pyinstaller/pyinstaller)
    - In folder with downloaded PyInstaller files run following commands:

    python setup.py build

    python setup.py install

    - Now go to folder with OMAD source files and run: "build_win.bat" to build binary and package it together with source into zip archive

