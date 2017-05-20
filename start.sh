#!/usr/bin/env python
if command -v python3 > /dev/null 2>&1; then
    python startup.py
else
    echo "Unable to locate python3. Please update to the latest version"
