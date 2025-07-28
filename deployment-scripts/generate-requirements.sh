#!/bin/bash
set -e

# Generate requirements.txt from pyproject.toml
echo "Generating requirements.txt from pyproject.toml..."
uv export --format requirements-txt --no-hashes --output-file requirements.txt

echo "requirements.txt generated successfully."
