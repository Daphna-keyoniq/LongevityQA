## Project uses CrewAI

CrewAI is a framework for building multi-agent systems with ease. It's a powerful tool for building AI agents that can collaborate on complex tasks.


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

To check whether all the tests pass, run: 

## Test

```bash
uv run pytest tests/
```