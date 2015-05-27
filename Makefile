
APTGET_RUN_DEP=python python-pip python-qt4
PIP_RUN_DEP=requests beautifulsoup4

APTGET_BUILD_DEP=$(APTGET_RUN_DEP) python-qt4-dev
PIP_BUILD_DEP=$(PIP_RUN_DEP) pyinstaller

ARCH=$(shell arch)
VERSION=$(shell python -c "import omad; print omad.__version__")

help:
	@echo "to install everything: \n\t make install"
	@echo "to install just app: \n\t make install_app"
	@echo "to install just dependencies: \n\t make install_dep"
	@echo "to uninstall app: \n\t make uninstall"
	@echo "to build to binary file: \n\t make build"
	@echo "to get build dependencies: \n\t make build_dep"
	@echo "to get development version of pyinstaller: \n\t make build_get_pyinstaller"

install: install_dep install_app
	
install_app: clean
	python setup.py build
	sudo python setup.py install
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
	sudo apt-get install git
	git clone https://github.com/pyinstaller/pyinstaller pyinstaller
	cd pyinstaller; python setup.py build
	cd pyinstaller; sudo python setup.py install
	sudo rm -rf pyinstaller

build: clean
	pyinstaller -F -w -n OMAD omad/__main__.py
	cp README* dist/ ; cp LICENSE* dist/
	cd dist; tar -zcvf ../OMAD_$(VERSION)_Linux_$(ARCH).tar.gz *
	
clean:
	rm -rf build dist
