# tools-in-action-Adkins
Quarto book + Python pipeline for STAT 4160 final project.

## Rendered Site:
https://kadkins3880.github.io/tools-in-action-Adkins/10_quarto_book.html

## Prerequisites
1. Python 3.10+ installed and on PATH.
2. Quarto CLI installed (https://quarto.org). Quarto is required to render and publish the book.
3. Git and GitHub account.
4. (Optional) GitHub CLI (`gh`) if you prefer authenticated Quarto publishes.

## Quickstart (fresh clone)
```bash
# 1. Clone repo
git clone https://github.com/kadkins3880/tools-in-action-Adkins.git
cd tools-in-action-Adkins

# 2. Create virtual environment & install Python deps
make env

# 3. Generate data, database, and features
make data
make db
make features

# 4. Render the Quarto book locally
make book

# 5. (Optional) Run tests
make test
