
APTGET_RUN_DEP=python3 python3-pip python3-pyqt4
PIP_RUN_DEP=requests beautifulsoup4

APTGET_BUILD_DEP=$(APTGET_RUN_DEP) python-qt4-dev
PIP_BUILD_DEP=$(PIP_RUN_DEP) pyinstaller

APTGET_TEST_DEP=python3-nose python3-coverage
PIP_TEST_DEP=

ARCH=$(shell arch)
VERSION=$(shell python3 -c "import omad; print omad.__version__")

help:
	@echo "Install everything: (Linux)\n\t make install"
	@echo "Install just app: (Linux)\n\t make install_app"
	@echo "Install just runtime dependencies: (Linux-Debian)\n\t make install_dep"
	@echo "Uninstall app: (Linux)\n\t make uninstall"
	@echo ""
	@echo "Build to static binary file: (Linux)\n\t make build"
	@echo "Get build dependencies: (Linux-Debian)\n\t make build_dep"

all: clean install_dep install install_test_dep

clean:
	sudo rm -rf build dist

install: clean
	sudo python3 setup.py build install
	sudo cp omad.desktop /usr/share/applications/omad.desktop

install_dep:
	sudo apt-get install $(APTGET_RUN_DEP)
	sudo pip3 install $(PIP_RUN_DEP)

install_test_dep:
	sudo apt-get install $(APTGET_TEST_DEP)
	#sudo pip3 install $(PIP_TEST_DEP)

uninstall:
	sudo pip3 uninstall omad
	sudo rm -f /usr/share/applications/omad.desktop
	sudo rm -f /usr/local/bin/omad

reinstall: uninstall install

run:
	PYTHONPATH=. python3 -m omad

## For Building Portable Application
####################################

# PyInstaller requires version >= 2.2 OR dev
# version 2.1 throws "import QtCore" error

build_dep:
	sudo apt-get install $(APTGET_BUILD_DEP)
	sudo pip3 install $(PIP_BUILD_DEP)

build: clean
	pyinstaller -D -n omad omad/__main__.py
	cp README* dist/ ; cp LICENSE* dist/ ; cp omad.desktop dist/
	git archive --format tar --output ./dist/omad_$(VERSION)_source.tar master
	cd dist; tar -zcvf ../omad_$(VERSION)_Linux_$(ARCH).tar.gz *

## For Development Only
#######################

test_all:
	PYTHONPATH=. nosetests3 -v --logging-level=INFO

test_all_coverage:
	PYTHONPATH=. nosetests3 -v --logging-level=INFO --with-coverage --cover-erase --cover-inclusive --cover-package=omad

test_mangafox:
	PYTHONPATH=. nosetests3 -v --logging-level=INFO -a site='mangafox'

test_batoto:
	PYTHONPATH=. nosetests3 -v --logging-level=INFO -a site='batoto'

test_mangatraders:
	PYTHONPATH=. nosetests3 -v --logging-level=INFO -a site='mangatraders'
