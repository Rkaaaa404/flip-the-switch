import json
from pathlib import Path

py_file = Path("models/model_2/03_model2_kaggle_pipeline.py")
ipynb_file = Path("models/model_2/03_model2_kaggle_pipeline.ipynb")

if not py_file.exists():
    py_file = Path("03_model2_kaggle_pipeline.py")
    ipynb_file = Path("03_model2_kaggle_pipeline.ipynb")

with open(py_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

cells = []
current_cell_type = None
current_source = []

def add_cell(cell_type, source_lines):
    if not source_lines:
        return
    # Strip empty lines from start and end
    content = "".join(source_lines).strip()
    if not content:
        return
    
    formatted_lines = [line + '\n' for line in content.split('\n')]
    if formatted_lines:
        formatted_lines[-1] = formatted_lines[-1].rstrip('\n')
        
    cells.append({
        "cell_type": cell_type,
        "metadata": {},
        "outputs": [] if cell_type == "code" else None,
        "execution_count": None if cell_type == "code" else None,
        "source": formatted_lines
    })

for line in lines:
    if line.startswith("# %% [markdown]"):
        if current_cell_type:
            add_cell(current_cell_type, current_source)
        current_cell_type = "markdown"
        current_source = []
    elif line.startswith("# %%"):
        if current_cell_type:
            add_cell(current_cell_type, current_source)
        current_cell_type = "code"
        current_source = []
    else:
        if current_cell_type == "markdown":
            # Remove leading '# ' or '#' from markdown cell content
            if line.startswith("# "):
                current_source.append(line[2:])
            elif line.startswith("#"):
                current_source.append(line[1:])
            else:
                current_source.append(line)
        elif current_cell_type == "code":
            current_source.append(line)

if current_cell_type:
    add_cell(current_cell_type, current_source)

# Clean outputs key for markdown cells
for cell in cells:
    if cell["cell_type"] == "markdown":
        cell.pop("outputs", None)
        cell.pop("execution_count", None)

notebook_json = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open(ipynb_file, 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, indent=2, ensure_ascii=False)

print(f"Berhasil mengonversi {py_file} -> {ipynb_file}")
