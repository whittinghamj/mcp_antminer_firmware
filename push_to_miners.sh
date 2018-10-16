#!/bin/bash

## MCP Antminer Firmware - DEV SCP Script

echo 'Pushing index.html to remote miners for dev.'

sshpass -p 'admin' scp index.html root@192.168.7.61:/www/pages/
sshpass -p 'admin' scp index.html root@192.168.7.66:/www/pages/

echo 'Done'
