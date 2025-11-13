# Liars Deck – Web Implementation & Reinforcement Learning(RL) Environment (WIP)

## Overview

This project is a web-based implementation of **Liars Deck**, a hidden-information card game built to run in the browser with a lightweight UI and minimal animations.  

The objectives of the project are:

1. Provide a playable web version of the game.
2. Use the same codebase as an **environment for training decision-making agents** (e.g. reinforcement learning bots) that can learn bluffing, risk management, and optimal play by self-play.
3. Enable play between bots and humans and track bot performance over time 

Right now the focus is on getting a clean, modular implementation of the game logic and a working web interface. The RL component is planned as the next stage.

---

## Current Features

- Python backend with clear separation of:
  - **game logic** (`src/`, `models/`)
  - **routes / endpoints** (`routes/`)
  - **presentation layer** (`templates/`, `static/`)
- Web UI for playing Liars Deck in the browser.
- Core game rules encoded in code (deck, turns, actions, resolving rounds).
- Designed so the same game logic can later be called from an RL training loop.

---

## Tech Stack

- **Python**
- **Web framework** (Flask-style app in `app.py`)
- **HTML / CSS / JS** for the frontend
- Modular structure for game logic and HTTP routes
