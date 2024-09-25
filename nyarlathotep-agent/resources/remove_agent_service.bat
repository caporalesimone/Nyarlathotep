@echo off
cls
cd /d %~dp0

rem Check if script is running with Admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires Admin privileges to be executed
    timeout 5
    exit /b 1
)

rem Set service name
set "serviceName=NyarlathotepAgent"

rem Checks if service exists
sc query %serviceName% >nul 2>&1
if %errorlevel% == 0 (
    echo Removing service ...
    nssm.exe stop %serviceName%
	nssm.exe remove %serviceName% confirm
	timeout 5
    exit /b 1
) else (
    echo Service not installed
	timeout 5
	exit /b 1
)

