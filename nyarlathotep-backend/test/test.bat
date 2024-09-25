@echo off
:loop
curl -X POST http://localhost:8080/client_update -H "Content-Type: application/json" -d @client_JSON_example.json
timeout /t 5 /nobreak >nul
goto loop


