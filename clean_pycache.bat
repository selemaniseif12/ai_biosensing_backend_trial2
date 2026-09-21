@echo off
echo Cleaning Python cache files...

for /r %%i in (*.pyc) do del /f /q "%%i"
for /d /r %%i in (__pycache__) do rmdir /s /q "%%i"

echo Done!
pause
