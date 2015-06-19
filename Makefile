
APTGET_RUN_DEP=python python-pip python-qt4
PIP_RUN_DEP=requests beautifulsoup

APTGET_BUILD_DEP=$(APTGET_RUN_DEP) python-qt4-dev
PIP_BUILD_DEP=$(PIP_RUN_DEP) pyinstaller

ARCH=$(shell arch)
VERSION=$(shell python -c "import omad; print omad.__version__")

help:
	@echo "Install everything: (Linux)\n\t make install"
	@echo "Install just app: (Linux)\n\t make install_app"
	@echo "Install just runtime dependencies: (Linux-Debian)\n\t make install_dep"
	@echo "Uninstall app: (Linux)\n\t make uninstall"
	@echo ""
	@echo "Build to static binary file: (Linux)\n\t make build"
	@echo "Get build dependencies: (Linux-Debian)\n\t make build_dep"

install: install_dep install_app
	
install_app: clean
	sudo python setup.py build install
	sudo cp omad.desktop /usr/share/applications/omad.desktop
	
install_dep: 
	sudo apt-get install $(APTGET_RUN_DEP)
	sudo pip install $(PIP_RUN_DEP)
	
uninstall:
	sudo pip uninstall omad
	sudo rm -f /usr/share/applications/omad.desktop
	sudo rm -f /usr/local/bin/omad

build_dep: 
	sudo apt-get install $(APTGET_BUILD_DEP)
	sudo pip install $(PIP_BUILD_DEP)
	
	$(eval PYINST_VER=$(shell python -c "import PyInstaller; v=PyInstaller.VERSION; print str(v[0])+str(v[1])") )
	$(eval PYINST_VER_DEV=$(shell python -c "import PyInstaller; v=PyInstaller.VERSION; print int('dev' in str(v))") )
	@echo "PyInstaller version: $(PYINST_VER), dev: $(PYINST_VER_DEV)"
	
	# PyInstaller requires version >= 2.2 OR dev
	# version 2.1 throws "import QtCore" error
	@if [ $(PYINST_VER_DEV) -ne 1 ] ; then \
		if [ ${PYINST_VER} -lt 22 ] ; then \
			echo "PyInstaller version is too low, installing development version from github";\
			make build_get_pyinstaller;\
		fi ;\
	fi
	
build_get_pyinstaller:
	sudo apt-get install git build-essential
	sudo rm -rf pyinstaller
	git clone https://github.com/pyinstaller/pyinstaller pyinstaller
	cd pyinstaller/bootloader ; python ./waf configure build install --no-lsb
	cd pyinstaller; sudo python setup.py build install

build: clean
	pyinstaller -D -n omad omad/__main__.py
	cp README* dist/ ; cp LICENSE* dist/ ; cp omad.desktop dist/
	git archive --format tar --output ./dist/omad_$(VERSION)_source.tar master
	cd dist; tar -zcvf ../omad_$(VERSION)_Linux_$(ARCH).tar.gz *
	
clean:
	sudo rm -rf build dist
