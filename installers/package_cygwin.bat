:: WARNING!! dont run this from ext4 network share

@echo off
set down_site=http://cygwin.mirrorcatalogs.com/
set app_name=manga_downloader
set app_arch=x86
::set app_arch=x86_64
set bash_script=package_cygwin_bash.sh

mkdir "%~dp0\%app_name%"
mkdir "%~dp0\%app_name%\cygwin"
mkdir "%~dp0\cygwin_down"

setup-x86_64.exe --quiet-mode --categories Base --packages wget --site "%down_site%" --arch "%app_arch%" --no-admin --no-shortcuts --root "%~dp0\%app_name%\cygwin" --local-package-dir "%~dp0\cygwin_down"

copy "%~dp0\%bash_script%" "%~dp0\%app_name%\cygwin\%bash_script%"
cd "%~dp0\%app_name%\cygwin\bin" 
bash.exe --login -c "chmod +x /%bash_script%"
bash.exe --login -c "/%bash_script%"
bash.exe --login -c "rm /%bash_script%"
cd "%~dp0"

echo @echo off > "%~dp0\%app_name%\manga_downloader.bat"
echo cd "%~dp0\%app_name%\cygwin\bin" >> "%~dp0\%app_name%\manga_downloader.bat"
echo bash.exe --login -c "./run.sh" >> "%~dp0\%app_name%\manga_downloader.bat"
