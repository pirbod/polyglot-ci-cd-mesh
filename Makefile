SHELL := /usr/bin/env bash
PYTHON ?= python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
NPM := npm

.PHONY: install test demo demo-check screenshots validate clean

install:
	$(PYTHON) scripts/install_local.py

test:
	$(PYTHON) scripts/run_all_tests.py

demo:
	$(PYTHON) scripts/bootstrap_demo.py

demo-check:
	$(PYTHON) scripts/demo_check.py

screenshots:
	$(PYTHON) scripts/capture_screenshots.py

validate:
	$(PYTHON) scripts/validate_repo_quality.py

clean:
	rm -rf $(VENV) dashboard/frontend/node_modules apps/node-service/node_modules docs/screenshots/*.svg
