@echo off
cd /d "%~dp0"
py server.py
if errorlevel 1 (
  echo.
  echo Python could not start. Check that Python is installed and the py command works.
  pause
)
