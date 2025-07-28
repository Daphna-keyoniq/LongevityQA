# MedAI Flow Makefile

# Variables
PYTHON = python
UV = uv
VENV = .venv
PYTEST = pytest
RUFF = ruff
MYPY = mypy
DOCKER = docker
DOCKER_COMPOSE = docker-compose

# Colors for terminal output
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

# Default target
.PHONY: help
help:
	@echo "$(GREEN)MedAI Flow Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@echo "  $(GREEN)make lint$(NC)          - Run linting checks"
	@echo "  $(GREEN)make test$(NC)          - Run all tests"
	@echo "  $(GREEN)make type-check$(NC)    - Run type checking"
	@echo "  $(GREEN)make docker-up$(NC)     - Start Docker containers"
	@echo "  $(GREEN)make docker-down$(NC)   - Stop Docker containers"
	@echo "  $(GREEN)make docker-rebuild$(NC) - Rebuild Docker containers"
	@echo "  $(GREEN)make run$(NC)           - Run the application"

# Linting
.PHONY: lint
lint:
	@echo "$(GREEN)Running linting checks...$(NC)"
	@$(UV) run $(RUFF) check --fix

# Testing
.PHONY: test
test:
	@echo "$(GREEN)Running all tests...$(NC)"
	@$(UV) run $(PYTEST) tests/

.PHONY: test-diagnose
test-diagnose:
	@echo "$(GREEN)Running diagnose crew tests...$(NC)"
	@$(UV) run $(PYTEST) tests/test_diagnose_crew.py

.PHONY: test-supplements
test-supplements:
	@echo "$(GREEN)Running supplements crew tests...$(NC)"
	@$(UV) run $(PYTEST) tests/test_supplements_crew.py

.PHONY: test-exercise
test-exercise:
	@echo "$(GREEN)Running exercise crew tests...$(NC)"
	@$(UV) run $(PYTEST) tests/test_exercise_crew.py

.PHONY: test-writer
test-writer:
	@echo "$(GREEN)Running writer crew tests...$(NC)"
	@$(UV) run $(PYTEST) tests/test_writer_crew.py

.PHONY: test-input-parser
test-input-parser:
	@echo "$(GREEN)Running input parser crew tests...$(NC)"
	@$(UV) run $(PYTEST) tests/test_input_parser_crew.py

.PHONY: test-api
test-api:
	@echo "$(GREEN)Running API tests...$(NC)"
	@$(UV) run $(PYTEST) tests/test_api.py

.PHONY: test-server
test-server:
	@echo "$(GREEN)Running server tests...$(NC)"
	@$(UV) run $(PYTEST) tests/test_server.py

# Type checking
.PHONY: type-check
type-check:
	@echo "$(GREEN)Running type checking...$(NC)"
	@$(UV) run $(MYPY) src --explicit-package-bases --pretty --show-error-codes

# Docker commands
.PHONY: docker-up
docker-up:
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	@$(DOCKER_COMPOSE) -f docker-compose.yml up

.PHONY: docker-down
docker-down:
	@echo "$(GREEN)Stopping Docker containers...$(NC)"
	@$(DOCKER_COMPOSE) -f docker-compose.yml down

.PHONY: docker-rebuild
docker-rebuild:
	@echo "$(GREEN)Rebuilding Docker containers...$(NC)"
	@$(DOCKER_COMPOSE) -f docker-compose.yml build

.PHONY: docker-clean
docker-clean:
	@echo "$(GREEN)Cleaning Docker resources...$(NC)"
	@$(DOCKER) rm -f $$($(DOCKER) ps -aq)
	@$(DOCKER) rmi -f $$($(DOCKER) images -q)
