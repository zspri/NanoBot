@ECHO off
title NanoBot
echo Checking pip for package updates...
pip install -U discord.py
pip install -U discord.py[voice]
pip install -U youtube-dl
echo done
timeout -t 5
python bot.py
start restart.bat
pause
exit