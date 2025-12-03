@echo off
echo Creating ZIP file for Citron_Tools addon...

rem Executes a PowerShell command to compress the contents of the Citron_Tools folder.
rem The key is '-Path ".\Citron_Tools\*"', which specifies "everything inside the folder".
rem This prevents the parent folder from being included in the ZIP file.
powershell -ExecutionPolicy Bypass -Command "Compress-Archive -Path '.\Citron_Tools\*' -DestinationPath '.\Citron_Tools.zip' -Force"

echo.
echo ----------------------------------------------------
echo Successfully created Citron_Tools.zip
echo You can now install this file in Blender or upload it to GitHub.
echo ----------------------------------------------------
echo.
pause
