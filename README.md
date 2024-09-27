# Nyarlathotep
Web remote workstations monitor 

## Description
This is a simple client, server (web) workstation monitor.

## Client aka Agent
It's a python application actually written for windows (will be os Independent)

## Backend Server
Backend server is a flask web server with 2 main route

- `/client_update` that waits for a POST with the JSON file from the client.
- `/workstations_status` that is an api that returns all the workstations information in a JSON 

## Frontend 
Frontend is written using node js, typescript and Svelte framework

