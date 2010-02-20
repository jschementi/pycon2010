call %~dp0clean.bat
pushd %~dp0gestalt
mklink /D dlr ..\bin3
mklink dlr.js ..\bin3\dlr.js
popd
