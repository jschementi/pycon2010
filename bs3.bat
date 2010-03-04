@echo off
msbuild %merlin_root%\Hosts\Silverlight\Silverlight4.sln /p:Configuration="Silverlight Release" /v:m %*

IF %ERRORLEVEL% NEQ 0 goto :END

copy /Y %merlin_root%\Bin\"Silverlight Release"\Chiron.exe %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\dlr.js %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\dlr.xap %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\IronPython.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\IronPython.Modules.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\IronPython.slvx %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\IronRuby.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\IronRuby.Libraries.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\IronRuby.slvx %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\Microsoft.Dynamic.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\Microsoft.Scripting.Core.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\Microsoft.Scripting.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\Microsoft.Scripting.ExtensionAttribute.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\Microsoft.Scripting.Silverlight.dll %~dp0bin3
copy /Y %merlin_root%\Bin\"Silverlight Release"\Microsoft.Scripting.slvx %~dp0bin3

%~dp0bin3\Chiron.exe /d:%~dp0oob /z:%~dp0oob.xap /n
%~dp0bin3\Chiron.exe /d:%~dp0rst2xaml\Silverlight\app /z:%~dp0rst2xaml\Silverlight\app.xap /n

:END
