@echo off
call :treeProcess
goto :eof

:treeProcess
for %%f in (*.tif) do echo %%f
for /D %%d in (*) do (
    cd %%d
    start mogrify -format bmp *
    call :treeProcess
    cd ..
)
exit /b