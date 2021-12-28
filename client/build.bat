@echo off
cd %~dp0
start env/Scripts/pyinstaller.exe --onefile client.py