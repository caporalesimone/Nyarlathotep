# Nyarlathotep
Web remote workstations monitor 

## Description
This is a simple client/server web based workstation monitor written in python.

## Server
Server is a flask web server waiting for a POST on the route `/client_update` containing a JSON file.
Each JSON file contains the status of a remote client and will be shown on a specifc card.


## Agent
To build a windows executable use auto-py-to-exe `pip install auto-py-to-exe`

