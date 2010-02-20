pushd %~dp0gestalt
if exist dlr    ( rmdir /S /Q dlr )
if exist dlr.js ( del dlr.js )
popd
