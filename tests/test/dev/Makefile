# -------------------------------------------
# pyr4t Development Makefile
# -------------------------------------------

# Variables
PYTHON := python
TYPE ?= all        # For clean (default: all)
ARGS ?=            # For run (optional extra arguments)

# -------------------------------------------
# Default target
# -------------------------------------------
help:
	@echo ""
	@echo "[help] Available commands:"
	@echo "  build             - Build project in dev mode with pip"
	@echo "  run ARGS="..."  - Run the main project script with optional args"
	@echo "  fmt               - Format code using black and isort"
	@echo "  clean TYPE=all    - Clean files: all, cache, log, tmp"
	@echo "  venv              - Create python venv on .venv"
	@echo ""

# -------------------------------------------
# Run main script
# -------------------------------------------
run:
	@echo "[info] Running main project..."
	$(PYTHON) -m test $(ARGS)
	@echo "[info] Run complete."

# -------------------------------------------
# Format code
# -------------------------------------------
fmt:
	$(PYTHON) -m scripts.manage -f

# -------------------------------------------
# Clean project
# -------------------------------------------
clean:
	$(PYTHON) -m scripts.manage -c $(TYPE)

# -------------------------------------------
# Create venv
# -------------------------------------------
venv:
ifeq ($(OS),Windows_NT)
	@if not exist "..\.venv" ( \
		echo [info] Creating virtual environment... && \
		$(PYTHON) -m venv ..\.venv && \
		echo [info] Venv creation complete. \
	) else ( \
		echo [info] Virtual environment already exists, skipping creation. \
	)
	@echo [info] To activate the venv: .\.venv\Scripts\activate
else
	@if [ ! -d "../.venv" ]; then \
		echo "[info] Creating virtual environment..."; \
		$(PYTHON) -m venv ../.venv; \
		echo "[info] Venv creation complete."; \
	else \
		echo "[info] Virtual environment already exists, skipping creation."; \
	fi
	@echo "[info] To activate the venv: source ./.venv/bin/activate"
endif

# -------------------------------------------
# Build project in dev mode
# -------------------------------------------
build:
	@echo "[info] Build in development mode..."
	$(PYTHON) -m pip install -e ..[dev]
	@echo "[info] Build complete."
