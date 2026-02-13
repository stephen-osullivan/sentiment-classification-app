# sentiment-classification-app
System for classifying sentiment based on the imdb dataset

**The below explains how to run the app with uv. To use docker see the DOCKER_DEPLOYENT.md**

## uv
1) Install: curl -LsSf https://astral.sh/uv/install.sh | sh
2) sync env: $ uv sync
3) run commands: $ uv run python main.py

## dvc
1) install: $ uv add dvc
2) initialise repo: $ uv run dvc init
3) run pipeline: $ uv run dvc 

## Launch fastapi app
$ uv run uvicorn apps.api.main:app --reload

## Curl the app with example request
$ curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This movie was absolutely amazing"}'

## Example app response:
{"label":"positive","confidence":0.729637729436262}

## Launch Streamlit Client
This allows you to send text to the fastapi api for realtime classification.

uv run streamlit run apps/client/app.py

## Tests
* Unit tests: $ uv run pytest tests/unit
* API tests: $ uv run pytests tests/api