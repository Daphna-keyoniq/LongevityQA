FROM python:3.9-slim

# Create the application directory
WORKDIR /medai_flow

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv directly and update PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Verify uv is installed correctly
RUN uv --version

# Copy pyproject.toml and uv.lock for dependency management
COPY pyproject.toml uv.lock ./

# Copy the source code AND knowledge directories
COPY src/ ./src/

# Create directories for input/output data
RUN mkdir -p input_data output_data logs/crews

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/medai_flow

# Expose API port
EXPOSE 8023

# Command to run the API
CMD ["uv", "run", "src/medai_flow/api.py"] 