python3 -c "import omad; print omad.__version__" > tmpFile
set /p VERSION= < tmpFile
del tmpFile
echo VERSION=%VERSION%

RMDIR /S /Q build
RMDIR /S /Q dist

pyinstaller -D -w -n omad omad/__main__.py
pyinstaller -D -n omad_cli omad/__main__.py

move .\dist\omad_cli\omad_cli.exe .\dist\omad\
move .\dist\omad_cli\omad_cli.exe.manifest .\dist\omad\
RMDIR /S /Q .\dist\omad_cli

copy .\README.* .\dist\
copy .\LICENSE.* .\dist\
git archive --format zip --output .\dist\omad_%VERSION%_source.zip master
python3 build_win_compress.py %VERSION% %PROCESSOR_ARCHITECTURE%
