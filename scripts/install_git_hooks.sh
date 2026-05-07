#!/bin/sh
set -eu

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push scripts/clean_notebook_outputs.py

echo "Git hooks installed from .githooks"
