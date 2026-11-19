@echo off
setlocal

set "SOURCE_DIR=%~dp0"
set "ZIP_FILE=%SOURCE_DIR%material_to_masked_groups.zip"

echo Building "%ZIP_FILE%"...

if exist "%ZIP_FILE%" del /Q "%ZIP_FILE%"
if errorlevel 1 goto :error

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ErrorActionPreference='Stop'; " ^
    "$source='%SOURCE_DIR%'; " ^
    "$zip='%ZIP_FILE%'; " ^
    "$staging=Join-Path $source '.build_staging'; " ^
    "if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }; " ^
    "New-Item -ItemType Directory -Path (Join-Path $staging 'modules') | Out-Null; " ^
    "New-Item -ItemType Directory -Path (Join-Path $staging 'plugins') | Out-Null; " ^
    "Copy-Item -Recurse -Force (Join-Path $source 'modules\*') (Join-Path $staging 'modules'); " ^
    "Copy-Item -Recurse -Force (Join-Path $source 'plugins\*') (Join-Path $staging 'plugins'); " ^
    "Get-ChildItem -Path $staging -Directory -Recurse -Filter '__pycache__' | Remove-Item -Recurse -Force; " ^
    "Get-ChildItem -Path $staging -File -Recurse -Filter '*.pyc' | Remove-Item -Force; " ^
    "Compress-Archive -Path (Join-Path $staging 'modules'),(Join-Path $staging 'plugins') -DestinationPath $zip -CompressionLevel Optimal; " ^
    "if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue }"
if errorlevel 1 goto :error

echo.
echo Build completed successfully.
exit /b 0

:error
echo.
echo Build failed.
exit /b 1