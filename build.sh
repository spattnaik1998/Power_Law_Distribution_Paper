#!/usr/bin/env bash
# Rebuild every table from the findings payloads, then compile the manuscript.
set -e
python paper/tables/_regenerate_tables.py
cd paper && latexmk -pdf main.tex
echo "-> paper/main.pdf"
