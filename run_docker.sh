#!/bin/bash

# # Docker build
# docker build --tag 'risktheodds' .

# # Define the path to the scores.json file
# SCORES_JSON_PATH="/path/to/scores.json"

# # Run the risktheodds Docker container with the scores.json file mounted
# docker run -v "$SCORES_JSON_PATH:/app/scores.json" -p 5098:5000 risktheodds

# Set variables
REPO_PATH="/opt/risktheodds"
DOCKER_COMPOSE_FILE="docker-compose.yml"
CONTAINER_NAME="risk-webapp"
SCORES_JSON_PATH="$(dirname $0)/data"

# Function to check for git changes
check_git_changes() {
  cd "$REPO_PATH"
  git fetch origin > /dev/null 2>&1
  if ! git diff --quiet origin/main; then
    echo "Changes detected in git repository."
    return 0
  else
    echo "No changes detected in git repository."
    return 1
  fi
}

# Function to pull changes and rebuild docker container
pull_and_rebuild() {
  cd "$REPO_PATH"
  git pull origin main
  docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache
  docker-compose -f "$DOCKER_COMPOSE_FILE" up -d --force-recreate "$CONTAINER_NAME"
  echo "Docker container rebuilt successfully."
}

# Main script
if check_git_changes; then
  pull_and_rebuild
else
  echo "