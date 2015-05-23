
help:
	@echo "to install everything: \n\t make install"
	@echo "to install just app: \n\t make install_app"
	@echo "to install just dependencies: \n\t make install_dep"
	@echo "to uninstall app: \n\t make uninstall"

install: install_dep install_app
	
install_app:
	sudo python setup.py install
	sudo cp omad.desktop /usr/share/applications/omad.desktop
	
install_dep: 
	sudo apt-get install python python-pip python-qt4 
	sudo pip install requests beautifulsoup4
	
uninstall:
	sudo pip uninstall omad
	sudo rm /usr/share/applications/omad.desktop
