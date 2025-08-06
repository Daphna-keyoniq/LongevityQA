
## Code Structure 

The app consists of a React Frontend and a Python Backend, which uses AI agents to generate answers to user questions. 
The backend uses a FastAPI server to handle communication with the frontend. 

The app contains two parts: 
1) Predefined questions and answers, specified under app/src/components/PredefinedQA.tsx
2) Chatbot questions and answers, using AI agents to process user questions and generate responses.

## Deployment

First expose the backend FastAPI server: 

```bash
gunicorn -k uvicorn.workers.UvicornWorker backend.api:app --bind 0.0.0.0:8011 --log-level debug --reload
```

Or if you want a stable version, that does not automatically change when the code changes: 

```bash
gunicorn -k uvicorn.workers.UvicornWorker backend.api:app --bind 0.0.0.0:8011 --log-level debug
```

You can verify that this works by running 

```bash
curl -X POST http://localhost:8011/ask -H "Content-Type: application/json" -d '{"question": "What is longevity?"}'
```

To deploy the frontend, first navigate to the "app" folder where the frontend code sits.

```bash
cd app
```

Then you can deploy the app using 

```bash
npm start
```

## Installation

Ensure you have Python >=3.9 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Then, running 

```bash
source .venv/bin/activate
```

Will activate the uv virtual enviroment medai-flow. 
In order to install all of the dependencies, run 


```bash
uv sync (--all-extras)
```
(Include all optional dependencies. Optional dependencies are defined via project.optional-dependencies in a pyproject.toml.)


## Lint

To check whether all the linting checks pass, run: 

```bash
uv run ruff check --fix
```


