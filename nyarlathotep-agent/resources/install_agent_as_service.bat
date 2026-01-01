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

rem Checks if NyarlathotepAgent exists
sc query NyarlathotepAgent >nul 2>&1
if %errorlevel% == 0 (
    echo Service already installed
    timeout 5
    exit /b 1
) 

echo Installing Nyarlathotep Agent as a service

rem Trova l'eseguibile Agent_*.exe (con versione)
for %%f in ("%~dp0Agent_*.exe") do set "appPath=%%~ff"

set "serviceName=NyarlathotepAgent"

nssm install %serviceName% "%appPath%"

nssm set %serviceName% AppDirectory %~dp0
nssm set %serviceName% AppThrottle 5000
nssm set %serviceName% Description "Nyarlathotep Agent - Workstation Monitor"
nssm set %serviceName% AppStopMethodConsole 1000

echo.
echo Starting Agent.
nssm start %serviceName%


nssm status %serviceName%
timeout 5
nssm status %serviceName%
timeout 5

