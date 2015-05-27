python -c "import omad; print omad.__version__" > tmpFile 
set /p VERSION= < tmpFile 
del tmpFile 
echo VERSION=%VERSION%

RMDIR /S /Q build
RMDIR /S /Q dist

pyinstaller -F -w -n omad omad/__main__.py

copy .\README.* .\dist\
copy .\LICENSE.* .\dist\
git archive --format zip --output .\dist\omad_%VERSION%_source.zip master
python build_win_compress.py %VERSION% %PROCESSOR_ARCHITECTURE%
