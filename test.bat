@echo off
setlocal

set "SOURCE_DIR=%~dp0"
set "PAINTER_PYTHON_DIR=%USERPROFILE%\Documents\Adobe\Adobe Substance 3D Painter\python"
set "PLUGIN_DIR=%PAINTER_PYTHON_DIR%\plugins"
set "MODULE_DIR=%PAINTER_PYTHON_DIR%\modules"

echo Deploying Materials to Masked Groups...
echo Destination: "%PAINTER_PYTHON_DIR%"

if not exist "%PLUGIN_DIR%" mkdir "%PLUGIN_DIR%"
if errorlevel 1 goto :error

if not exist "%MODULE_DIR%" mkdir "%MODULE_DIR%"
if errorlevel 1 goto :error

copy /Y "%SOURCE_DIR%plugins\mat2msk_launcher.py" "%PLUGIN_DIR%\mat2msk_launcher.py" >nul
echo Plugin copied to "%PLUGIN_DIR%\mat2msk_launcher.py"
if errorlevel 1 goto :error

if not exist "%MODULE_DIR%\mat2msk" mkdir "%MODULE_DIR%\mat2msk"
if errorlevel 1 goto :error

xcopy /Y /I /E "%SOURCE_DIR%modules\mat2msk" "%MODULE_DIR%\mat2msk" >nul
if errorlevel 1 goto :error

xcopy /Y /I "%SOURCE_DIR%modules\__init__.py" "%MODULE_DIR%\" >nul
if errorlevel 1 goto :error

echo.
echo Deployment completed successfully.
echo Substance 3D Painter needs to be restarted before testing the plugin.
exit /b 0

:error
echo.
echo Deployment failed.
exit /b 1
