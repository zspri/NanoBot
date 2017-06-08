@ECHO off
echo Restarting...
title NanoBot
PING 1.1.1.1 -n 1 -w 3000 >NUL
python bot.py