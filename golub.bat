@echo off
chcp 65001 > nul
title 🕊️ Love Pigeon
cls

echo.
echo ************************************
echo *          🕊️ курлык!              *
echo ************************************
echo.

set /p answer=Do you love pigeon? (yes/no): 

if /i "%answer%"=="yes" (
    cls
    color 0C
    echo.
    echo     ураааааааааааа!
    echo.
    color 07
) else (
    cls
    echo.
    echo     😔 Oh no... Pigeon is sad.
    echo.
)

echo.
echo Press any key to exit...
pause > nul
exit
