# Makefile for STAT4160 final project (Quarto book + Python pipeline)
# Usage: make <target>
# Common targets: help env data db features book publish test lint clean

.DEFAULT_GOAL := help

.PHONY: help env data db features book publish test lint clean

help:
	@echo "Available targets:"
	@echo "  env       Create virtualenv and install Python dependencies"
	@echo "  data      Generate raw/synthetic data (runs scripts/make_synth_data.py)"
	@echo "  db        Create/populate sqlite DB (runs scripts/make_sqlite.py)"
	@echo "  features  Build feature files (runs scripts/build_features.py)"
	@echo "  book      Render the Quarto book (quarto render book)"
	@echo "  test      Run pytest"
	@echo "  clean     Remove build artifacts, venv, and generated data"

env:
	pip install -r requirements.txt
data:
	python scripts/make_synth_data.py
db:
	python scripts/make_sqlite.py
features:
	python scripts/build_features.py
book:
	quarto render book
test:
	pytest -q
clean:
	rm -rf db/*.db data/processed/* book/_site book/_freeze