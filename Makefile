# -------------------------------------------
# pyr4t Makefile
# -------------------------------------------

# Variables
PYTHON := python
MODE ?= classic    # For build (optional extra arguments)

# -------------------------------------------
# Default target
# -------------------------------------------
help:
	@echo ""
	@echo "[help] Available commands:"
	@echo "  build MODE=prod   - Build project in prod mode with pip"
	@echo "  test              - Run tests"
	@echo ""

# -------------------------------------------
# Build project
# -------------------------------------------
build:
	@echo "[info] Build in production mode..."
	$(PYTHON) -m pip install .
	@echo "[info] Build complete."

# -------------------------------------------
# Run test scripts
# -------------------------------------------
test:
	@echo "[info] Running test scripts..."
	$(PYTHON) -m scripts.manage -t
	@echo "[info] Tests complete."
