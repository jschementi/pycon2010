msbuild %merlin_root%\Hosts\Silverlight\Silverlight4.sln /p:Configuration="Silverlight 4 Release" /p:SilverlightPath="%merlin_root%\utilities\silverlight\v4-internal-x86fre" %*
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\dlr.js %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\dlr.xap %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\IronPython.dll %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\IronPython.Modules.dll %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\IronPython.slvx %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\IronRuby.dll %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\IronRuby.Libraries.dll %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\IronRuby.slvx %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\Microsoft.Dynamic.dll %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\Microsoft.Scripting.dll %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\Microsoft.Scripting.Silverlight.dll %~dp0bin
copy /Y %merlin_root%\Bin\"Silverlight 4 Release"\Microsoft.Scripting.slvx %~dp0bin
