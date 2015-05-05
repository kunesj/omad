#!/bin/bash
packages_apt="xorg-server xinit xorg-docs xlaunch git python python-pyqt4"
packages_pip="requests beautifulsoup4"

# install commandline package manager
wget raw.githubusercontent.com/transcode-open/apt-cyg/master/apt-cyg -O apt-cyg --no-check-certificate
chmod +x apt-cyg
mv apt-cyg /usr/local/bin/

# install python+pip
apt-cyg update
apt-cyg install python python-setuptools
easy_install pip

# install packages apt+pip
apt-cyg install $packages_apt
pip install $packages_pip

# download source from github and install
rm -r -f manga_downloader
git clone https://github.com/kunesj/manga_downloader.git manga_downloader
cd manga_downloader
make install_app
cd ..

# create xserver run configuration
echo '<?xml version="1.0" encoding="UTF-8"?>
<XLaunch WindowMode="MultiWindow" ClientMode="StartProgram" LocalClient="True" Display="0" RemoteProtocol="" LocalProgram="manga_downloader" RemoteProgram="manga_downloader" RemoteHost="" RemoteUser="" XDMCPHost="" XDMCPBroadcast="False" XDMCPIndirect="False" Clipboard="True" ExtraParams="" Wgl="True" DisableAC="False" XDMCPTerminate="False" SSHKeyChain="False" SSHTerminal="False" ExtraSSH=""/>' > manga_downloader.xlaunch

echo "#!/bin/bash" > run.sh
echo "xlaunch -run manga_downloader.xlaunch" >> run.sh
chmod +x run.sh
