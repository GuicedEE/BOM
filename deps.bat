@echo off
echo Checking for dependency updates...
call mvn versions:display-dependency-updates

echo.
echo Checking for plugin updates...
call mvn versions:display-plugin-updates

echo.
echo Checking for property updates...
call mvn versions:display-property-updates

pause