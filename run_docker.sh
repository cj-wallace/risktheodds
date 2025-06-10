#!/bin/bash

# Docker build
docker build --tag 'risktheodds' .

# Define the path to the scores.json file
SCORES_JSON_PATH="/path/to/scores.json"

# Run the risktheodds Docker container with the scores.json file mounted
docker run -v "$SCORES_JSON_PATH:/app/scores.json" -p 5098:5000 risktheodds