#!/bin/bash
set -e  # Exit on any error

# Install PDM
pip install pdm

# Install and build the project
make install 
make build