#!/usr/bin/env python3
"""Build and EXECUTE the procedural-layer notebooks from specs/*.json.

Pipeline (raw JSON -> execute -> output): each spec is a list of md/code cells;
we assemble a v4 notebook with nbformat, run it top to bottom with nbclient
(allow_errors=True so INTENDED ERROR cells keep their real traceback as output),
then write the executed .ipynb next to this script.

A cell whose source contains 'INTENDED ERROR' may raise - that traceback IS the
lesson. Any error in a cell without that marker is reported as a build failure.

Usage: python3 make_notebooks.py [spec.json ...]   (default: specs/*.json)
Requires: pip install nbformat nbclient ipykernel
"""
import glob
import json
import os
import sys

import nbformat
from nbclient import NotebookClient

HERE = os.path.dirname(os.path.abspath(__file__))


def build(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    for cell in spec["cells"]:
        src = cell["source"]
        if cell["type"] == "md":
            nb.cells.append(nbformat.v4.new_markdown_cell(src))
        else:
            nb.cells.append(nbformat.v4.new_code_cell(src))

    client = NotebookClient(nb, timeout=90, allow_errors=True, kernel_name="python3")
    client.execute()

    unexpected = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        errs = [o for o in cell.get("outputs", []) if o.get("output_type") == "error"]
        if errs and "INTENDED ERROR" not in cell.source:
            unexpected.append((i, errs[0].get("ename"), errs[0].get("evalue", "")[:80]))

    out = os.path.join(HERE, spec["notebook"] + ".ipynb")
    nbformat.write(nb, out)
    return out, unexpected


def main():
    specs = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "specs", "*.json")))
    failed = False
    for s in specs:
        out, unexpected = build(s)
        status = "OK" if not unexpected else f"UNEXPECTED ERRORS: {unexpected}"
        print(f"{os.path.basename(out)}: {status}")
        failed = failed or bool(unexpected)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
