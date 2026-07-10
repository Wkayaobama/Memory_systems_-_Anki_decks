# Programming Millenium

A refactor of the [Millenium system](../01.Millenium/) for **programming principles**: the same
memory components, the same spreadsheet matrix — but instead of 1000 numbers mapped to images,
1000 programming concepts mapped to fixed 3-digit addresses with vivid anchor images.

## The original matrix, decoded

`MIllenium_20220203.xlsx` (tab `millenium`, rows 2–1001 = numbers 0–999):

| Col | Original header | Role |
|-----|-----------------|------|
| A | *(flag)* + `=SUM(A2:A1003)` at row 1004 | learned yes/no + progress total |
| B | `Nbre` | fixed address space 0–999 |
| C | `Objet - Personnage` | ONE canonical vivid image per address |
| D | `attention doublon` | collision registry ("nid déjà pris") |
| E | `non retenu mais convient` | valid alternates kept on the bench |
| F | `autre idée mais difficile à utiliser` | rejected ideas, kept to avoid re-evaluating |
| N/O/P | `A FAIRE` / `!!!!` / `done` | far-column backlog of sources to mine |
| tab `tuto` | 6 steps | export pipeline: spreadsheet → txt → Anki (Anki comes LAST) |

The generative rule (French Major-system phonetics, in `millenium.ipynb`) lives outside the
sheet: digits → consonant sounds → candidate words → curated image.

## The refactor: same components, programming payload

| Memory component | Original | Programming Millenium |
|------------------|----------|----------------------|
| Generative encoding rule | phonetic code digits→sounds | **decimal taxonomy**: hundreds = domain, tens = category, units = item (0 = most fundamental) |
| Fixed address space | numbers 0–999 | codes 000–999 (10 domains × 10 categories × 10 concepts) |
| Canonical payload (col C) | one image per number | one **concept** per code + one **anchor image** encoding its mechanism/name |
| attention doublon (col D) | "déjà pris" warnings | confusables column: nearest confused concept + the one discriminating difference, and `cf. XXX (déjà pris)` cross-references |
| non retenu (col E) | alternate words | alternate anchor images considered |
| difficile à utiliser (col F) | hard ideas | free column for your own rejects |
| Learned flag + SUM | col A, 809/1000 | col A, starts at 0/1000 — same `=SUM` at row 1004 |
| Backlog N/O/P | source lists | seeded with next steps (images, per-language variants…) |
| tuto tab | txt → Anki | `build.py` → `export_for_anki/*.csv` → Anki (still last) |

Digit mnemonics for the hundreds (the "phonetics" of this system):
**0** fundamentals (null, the origin) · **1** data structures (a single node) · **2** algorithms
(binary: compare two, split in two) · **3** functions/FP (input→transform→output) · **4** OOP
(four pillars) · **5** concurrency (five dining philosophers) · **6** architecture (six sides of
the hexagon) · **7** data & persistence (seven normal forms) · **8** networking/distributed
(port 80, ∞ machines) · **9** quality/security/ops (five nines).
Code **000** = "Value", code **999** = "Blameless postmortem". The full 10×10 category grid is
in the workbook's `taxonomy` tab.

Recall routes it trains, both directions:
- code → domain/category digits → concept (and concept → its address);
- anchor scene bridges the two — and you can **fuse it with your existing French Millenium peg**
  for the same number (e.g. 042 *raie/…* + the do-while soup-tasting scene) to bind address ↔ concept.

## Files

- `programming_millenium.csv` — source of truth, one row per code (edit here)
- `Programming_Millenium.xlsx` — tabs `matrix` / `taxonomy` / `tuto` (generated)
- `export_for_anki/000.csv … 900.csv` — semicolon-separated per-hundred blocks, same shape as
  the original export (`code;concept;anchor;definition;example;confusables`)
- `build.py` — regenerates the xlsx + exports from the CSV (`pip install openpyxl`)

Content was drafted by one authoring pass per domain, then de-duplicated ("one concept, one
home") and cross-referenced. Expect to tweak entries as you learn — that's the point of the
matrix: the spreadsheet is the living source, Anki is just the drill.
