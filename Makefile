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
	@echo "  publish   Publish book to GitHub Pages (quarto publish gh-pages)"
	@echo "  test      Run pytest"
	@echo "  lint      Run code style checks (black --check)"
	@echo "  clean     Remove build artifacts, venv, and generated data"

# Create a lightweight virtual environment and install pinned packages
env:
	python -m venv .venv
	.venv\Scripts\activate && python -m pip install --upgrade pip
	.venv\Scripts\activate && pip install -r requirements.txt

# Generate synthetic/raw data (script should write into data/raw/)
data:
	@echo "Running data generation script..."
	.venv\Scripts\activate && python scripts/make_synth_data.py

# Create or populate a sqlite database (script should write into db/)
db:
	@echo "Creating sqlite database..."
	.venv\Scripts\activate && python scripts/make_sqlite.py

# Build features from raw data into data/processed/
features:
	@echo "Building features..."
	.venv\Scripts\activate && python scripts/build_features.py

# Render the Quarto book (assumes Quarto CLI installed on system)
book:
	@echo "Rendering Quarto book..."
	quarto render book

# Publish the book to GitHub Pages (Quarto will push to gh-pages branch)
# Note: quarto publish gh-pages requires gh CLI authentication or previously configured git remote.
publish:
	@echo "Publishing book to GitHub Pages (book/ -> gh-pages)..."
	cd book && quarto publish gh-pages --no-prompt

# Run test suite (pytest)
test:
	.venv\Scripts\activate && pytest -q

# Lint/format check
lint:
	.venv\Scripts\activate && black --check .

# Remove virtualenv and generated artifacts
clean:
	@echo "Cleaning up..."
	rm -rf .venv
	rm -rf book/_site book/_freeze
	rm -rf data/processed data/*.parquet data/*.csv
	rm -rf db/*.db