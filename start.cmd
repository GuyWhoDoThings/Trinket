@echo off
TITLE Trinket Server Software
if exist startup.py (
  python startup.py
) else (
  echo "[ERROR] Unable to locate startup.py"
  pause
  exit 2
)
