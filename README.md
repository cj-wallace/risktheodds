# RiskTheOdds

Welcome to the RiskTheOdds project! This repository contains the source code and documentation for the RiskTheOdds webapp game.

## Overview

RiskTheOdds is a web-based game built in Flask. It aims to be a fun web game that can be picked up and put down whenever! The app is built as a full-stack web app so that there is integration with a server-side leaderboard that updates when users submit their high scores.

The tools used include Python, Flask, SQLite, Django, and Jinja.

![Opening Screen](/assets/readme/screenshot_1.png "Opening Screen")

## Features

- Feature 1: Stake your current balance against a random odds generator to win and increase your score!
- Feature 2: Progress is saved in browser using session data.
- Feature 3: Once you are done, you can cash out your score and be added to the backend high score list!

## Installation

To install and run this project locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/cj-wallace/risktheodds.git
    ```
2. Navigate to the project directory:
    ```sh
    cd risktheodds/webapp
    ```
3. Run docker build:
    ```sh
    docker build --tag 'risktheodds' .
    ```
4. Run the application:
    ```sh
    mkdir data
    touch data/scores.json
    SCORES_JSON_PATH="data/"
    docker run -d -v "$SCORES_JSON_PATH:/app/data/" -p 5000:5000 --name risktheodds risktheodds

    ```

## Images

Game Screen
![Game Screen](/assets/readme/screenshot_2.png "Game Screen")

High Score Page
![High Scores Page](/assets/readme/screenshot_3.png "High Scores Page")