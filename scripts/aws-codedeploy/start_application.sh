#!/bin/bash

# AWS Code Deploy 'ApplicationStart' step, see: appspec.yml
sh scripts/start_server.sh

# exit venv
deactivate
