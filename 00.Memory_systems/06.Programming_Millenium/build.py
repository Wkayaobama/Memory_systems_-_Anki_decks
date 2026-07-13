#!/usr/bin/env python3
"""Build Programming_Millenium.xlsx and export_for_anki/ from programming_millenium.csv.

Source of truth: programming_millenium.csv (one row per code 000-999).
This mirrors the original Millennium pipeline (millenium.ipynb -> csv -> xlsx -> Anki
exports): the spreadsheet is the curation matrix, the exports feed Anki last.

Usage: python3 build.py          (requires: pip install openpyxl)
"""
import csv
import os

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "programming_millenium.csv")
XLSX_PATH = os.path.join(HERE, "Programming_Millenium.xlsx")
EXPORT_DIR = os.path.join(HERE, "export_for_anki")

# Column layout of the matrix tab; groups mirror the original millenium tab:
#   A Learned flag (col A + SUM row) | B code (Nbre) | C-F payload (Objet-Personnage,
#   enriched) | G doublon (attention doublon) | H alternates (non retenu mais convient)
#   | I rejected (autre idee difficile a utiliser) | J-K taxonomy helpers | N-P backlog
HEADERS = [
    ("A", "Learned (0/1)"),
    ("B", "Code"),
    ("C", "Concept"),
    ("D", "Anchor (mental image)"),
    ("E", "Definition"),
    ("F", "Example"),
    ("G", "Attention doublon / confusables"),
    ("H", "Non retenu mais convient (alt. anchors)"),
    ("I", "Autre idée difficile à utiliser"),
    ("J", "Domain"),
    ("K", "Category"),
    ("N", "A FAIRE"),
    ("O", "!!!!"),
    ("P", "done"),
]
WIDTHS = {"A": 11, "B": 7, "C": 28, "D": 52, "E": 52, "F": 42, "G": 40, "H": 34,
          "I": 26, "J": 30, "K": 30, "N": 34, "O": 6, "P": 7}

BACKLOG = [
    ("per-language variants (Python/JS/Go) as extra columns", "", ""),
    ("draw or generate a picture per anchor", "", ""),
    ("fuse each code with the French Millenium peg image (00.Memory_systems/01.Millenium)", "!!!!", ""),
    ("review confusables after first learning pass", "", ""),
    ("mark Learned=1 as codes are memorized; SUM at bottom tracks progress", "", "done"),
]

TUTO = [
    (1, "csv", "programming_millenium.csv is the source of truth - edit it (or the matrix tab, then re-export)"),
    (2, "python", "run build.py to regenerate this workbook and export_for_anki/*.csv (already UTF-8, no notepad step needed)"),
    (3, "anki", "create new deck 'Programming Millenium'"),
    (4, "anki", "tools -> manage note types -> add (clone basic) -> rename -> fields: Code, Concept, Anchor, Definition, Example, Confusables"),
    (5, "anki", "cards: front = {{Code}} (and a second template front = {{Concept}}), back = the rest"),
    (6, "anki", "file -> import each export_for_anki/*.csv (semicolon-separated, fields mapped in order) into a subdeck per hundred"),
    ("", "tip", 'concat like the original: front can be Code & " " & Concept'),
    ("", "", ""),
    ("3rd way", "excel", "multi-card import (see README 'Pathway 3'): save the matrix tab as tab-delimited .txt, re-saved as UTF-8"),
    ("3rd way", "anki", "manage note types -> clone Basic (the '10 Question' type is not in the repo - recreating it IS these steps) -> fields = Code, Concept, Anchor, Definition, Example, Confusables IN COLUMN ORDER"),
    ("3rd way", "anki", "cards: one template per question, front wrapped in a conditional so blanks make no card: {{#Definition}}Definition of {{Code}} {{Concept}}?{{/Definition}}"),
    ("3rd way", "anki", "back: {{FrontSide}} <hr id=answer> {{Definition}} - repeat per column; reverse card {{#Concept}}Address of {{Concept}}?{{/Concept}} -> {{Code}}"),
    ("3rd way", "anki", "file -> import the .txt (separator Tab, note type = the clone, fields map in order); each note yields one card per non-blank template"),
    ("more advanced", "youtube", "Converting a COMPLEX Excel file to an Anki deck! - YouTube"),
]


def read_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1000, f"expected 1000 rows, got {len(rows)}"
    return rows


def build_matrix_sheet(ws, rows):
    bold = Font(bold=True)
    fill = PatternFill("solid", fgColor="DDEBF7")
    for col, title in HEADERS:
        c = ws[f"{col}1"]
        c.value = title
        c.font = bold
        c.fill = fill
    for i, r in enumerate(rows, start=2):
        ws[f"A{i}"] = int(r.get("learned", 0) or 0)
        ws[f"B{i}"] = r["code"]
        ws[f"C{i}"] = r["concept"]
        ws[f"D{i}"] = r["anchor"]
        ws[f"E{i}"] = r["definition"]
        ws[f"F{i}"] = r["example"]
        ws[f"G{i}"] = r["confusables"]
        ws[f"H{i}"] = r["alternates"]
        ws[f"J{i}"] = r["domain_name"]
        ws[f"K{i}"] = r["category_name"]
    # progress SUM at row 1004, same spot as the original sheet
    ws["A1004"] = "=SUM(A2:A1003)"
    ws["B1004"] = "learned / 1000"
    for j, (todo, bang, done) in enumerate(BACKLOG, start=2):
        ws[f"N{j}"], ws[f"O{j}"], ws[f"P{j}"] = todo, bang, done
    for col, w in WIDTHS.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = "A1:P1001"


def build_taxonomy_sheet(ws, rows):
    bold = Font(bold=True)
    fill = PatternFill("solid", fgColor="FCE4D6")
    ws["A1"] = "The code IS the mnemonic: hundreds digit = domain, tens = category, units = item (0 = most fundamental)."
    ws["A2"] = "Retrieval route: code -> digit mnemonics -> category -> concept, or fuse the code's French Millenium peg image (01.Millenium) with the Anchor scene."
    ws["A1"].font = bold
    # domain/mnemonic table + 10x10 category grid
    ws["A4"], ws["B4"], ws["C4"] = "Digit", "Domain", "Digit mnemonic"
    for c in ("A4", "B4", "C4"):
        ws[c].font, ws[c].fill = bold, fill
    domains, cats = {}, {}
    for r in rows:
        domains[r["code"][0]] = (r["domain_name"], r["mnemonic"])
        cats[r["code"][:2]] = r["category_name"]
    for d in sorted(domains):
        ws[f"A{5 + int(d)}"], ws[f"B{5 + int(d)}"], ws[f"C{5 + int(d)}"] = int(d), *domains[d]
    ws["A17"] = "Category grid (row = domain digit, column = tens digit)"
    ws["A17"].font = bold
    for t in range(10):
        c = ws.cell(row=18, column=2 + t, value=f"_{t}_")
        c.font, c.fill = bold, fill
    for d in range(10):
        ws.cell(row=19 + d, column=1, value=f"{d}xx").font = bold
        for t in range(10):
            ws.cell(row=19 + d, column=2 + t, value=cats.get(f"{d}{t}", ""))
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 70
    for t in range(10):
        ws.column_dimensions[get_column_letter(2 + t)].width = 26


def build_tuto_sheet(ws):
    for i, (nb, tool, action) in enumerate(TUTO, start=2):
        ws[f"A{i}"], ws[f"B{i}"], ws[f"C{i}"] = nb, tool, action
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 120


def export_anki(rows):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    for h in range(10):
        block = [r for r in rows if r["code"][0] == str(h)]
        path = os.path.join(EXPORT_DIR, f"{h}00.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            for r in block:
                w.writerow([r["code"], r["concept"], r["anchor"], r["definition"],
                            r["example"], r["confusables"]])


def main():
    rows = read_rows()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "matrix"
    build_matrix_sheet(ws, rows)
    build_taxonomy_sheet(wb.create_sheet("taxonomy"), rows)
    build_tuto_sheet(wb.create_sheet("tuto"))
    wb.save(XLSX_PATH)
    export_anki(rows)
    print(f"wrote {XLSX_PATH} and {EXPORT_DIR}/*.csv from {len(rows)} rows")


if __name__ == "__main__":
    main()
