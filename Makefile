
APTGET_RUN_DEP=python python-pip python-qt4
PIP_RUN_DEP=requests beautifulsoup4

APTGET_BUILD_DEP=$(APTGET_RUN_DEP) python-qt4-dev
PIP_BUILD_DEP=$(PIP_RUN_DEP) pyinstaller

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
	
build_get_pyinstaller:
	sudo apt-get install git
	git clone https://github.com/pyinstaller/pyinstaller pyinstaller
	cd pyinstaller; python setup.py build
	cd pyinstaller; sudo python setup.py install
	sudo rm -rf pyinstaller

#pyinstaller requires version >= 2.2 OR dev
build: clean
	pyinstaller -F -w -n OMAD omad/__main__.py
	@echo ""
	@echo "If getting QtCore import error when running, run: make build_get_pyinstaller"
	
clean:
	rm -rf build dist
