@echo off
setlocal
cd /d "%~dp0"
echo.
echo NEXUS PERSONA V10 - INICIANDO...
echo.
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  start "" "http://127.0.0.1:8765/"
  py -3 -m http.server 8765 --bind 127.0.0.1
  goto :end
)
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  start "" "http://127.0.0.1:8765/"
  python -m http.server 8765 --bind 127.0.0.1
  goto :end
)
echo Python nao foi encontrado. Abra o arquivo index.html
echo no Chrome ou Edge. Se o microfone nao funcionar,
echo instale o Python ou execute a aplicacao em servidor HTTPS.
pause
:end
endlocal
