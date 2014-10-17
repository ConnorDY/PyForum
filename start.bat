@echo off
start "" "C:/MongoDB/bin/mongod.exe" --dbpath C:/MongoDB/data/db
python server.py
pause