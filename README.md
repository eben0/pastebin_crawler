# Pastebin Crawler

This a sample pastebin crawler that crawles the recent pastes from the homepage.

## Prerequisites
- python3
- a cup of coffee (mandatory!!!)

## Running the crawler
1. It is recommended to create a virtual environment
```
    python -m venv venv
    source ./venv/bin/activate
```

2. Installing dependencies
```
    cd src/
    pip -r requirements.txt
```

3. Running the crawler
```
    cd src/
    python main.py
```

## Running the crawler with docker compose
```
docker compose up
```

## Linting & Formatting
Use flake8 for linting and black for formatting
```
    cd src/
    pip -r requirements-dev.txt
    black -l 79 <file>.py
    flake8 .
```

## Config

1. The crawler uses the following yaml file format
```yaml
# location: ../assets/config.yaml
crawler:
  # URL of the site to crawl
  url: https://pastebin.com
  # where to save the paste content
  pastes_path: ../assets/pastes
  # time to repeat the action
  interval: 120

db:
  file: ../assets/db/pastes_db.json
  table: pastes


logger:
  name: PastebinCrawler
  level: INFO
```
2. To change the path of the config file, set the environment variable:
```
CONFIG_PATH=../assets/config.yaml
```
