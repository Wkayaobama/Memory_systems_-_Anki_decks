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

### How an anchor fuses the address with its concept

The two halves carry different information, and mixing them up is the main source of
confusion: **the digits are decoded by the taxonomy, never by the anchor.** Read a code left
to right — hundreds digit → domain (via its digit mnemonic), tens digit → category (the
domain's shelf, ordered fundamentals → advanced), units digit → rank on that shelf (0 = most
fundamental). That walk alone lands you on the right shelf. The **anchor encodes only the
concept** — its mechanism or its name — as one vivid scene. Fusion happens when you *place
that scene at the address*: stage the anchor inside the domain's mnemonic setting, or
(stronger, both directions) merge it with your existing French Millenium peg image for that
exact number — peg(number) × anchor(concept) = one compound image that answers both
"what lives at 520?" and "where does mutex live?". Three worked examples:

- **520 Mutex** — address walk: 5 = the dining-philosophers table (concurrency), category
  x2 = the locks shelf, units 0 = the most fundamental lock. Anchor (concept only): *a
  restroom key chained to your own belt loop — only you can hang it back* (= ownership, the
  thing that makes a mutex a mutex). Fuse: the philosophers' restroom key.
- **253 Memoization** — 2 = algorithms (compare two, split in two), x5 = the dynamic-programming
  shelf, rank 3. Anchor puns the NAME: *a student tapes a MEMO to the fridge and skips the
  math at the next midnight craving* — "memo" gives you the word back, the lazy fridge gives
  you the mechanism.
- **999 Blameless postmortem** — 9 = five nines (never failing), x9 = observability & ops,
  rank 9: the very last slot of the matrix. Its anchor fuses on its own: *surgeons dissect
  the fallen server's organs, never the intern's hands — five nines end not in punishment but
  in learning*. The address ("the end of everything") and the concept ("what you do at the
  end") reinforce each other.

Recall routes it trains, both directions:
- code → domain/category digits → concept (and concept → its address);
- anchor scene bridges the two — and you can **fuse it with your existing French Millenium peg**
  for the same number (e.g. 042 *raie/…* + the do-while soup-tasting scene) to bind address ↔ concept.

## The procedural layer: notebooks

Imagery and definitions are declarative memory; **seeing the net effect of code you run is
procedural memory** — the same reason this repo is built out of `.ipynb` notebooks. One
notebook per hundred-block (same chunking as `export_for_anki/`), and from each category
exactly ONE carefully chosen **engraver concept** — the demo whose input→output burns in the
*larger* idea, not the particulars (`037 Nesting depth` teaches all of branching;
`716 EXPLAIN before/after an index` teaches all of query performance):

```
notebooks/000_fundamentals.ipynb … 900_quality_ops.ipynb   (10 × 10 demos, executed outputs committed)
```

Method per cell: read the code → **predict the output** → run → compare. Cells marked
`# INTENDED ERROR — read the traceback` raise on purpose: the traceback IS the lesson
(off-by-one `IndexError`, duplicate-key `IntegrityError`, port-in-use `OSError`…).
The pipeline is raw JSON → execute → output: `notebooks/specs/*.json` hold the cells,
`notebooks/make_notebooks.py` assembles them with nbformat and executes them with nbclient,
committing notebooks *with* their outputs so review works without running anything.

## Files

- `programming_millenium.csv` — source of truth, one row per code (edit here)
- `Programming_Millenium.xlsx` — tabs `matrix` / `taxonomy` / `tuto` (generated)
- `export_for_anki/000.csv … 900.csv` — semicolon-separated per-hundred blocks, same shape as
  the original export (`code;concept;anchor;definition;example;confusables`)
- `build.py` — regenerates the xlsx + exports from the CSV (`pip install openpyxl`)
- `notebooks/` — the procedural layer: specs + builder + 10 executed notebooks
  (`pip install nbformat nbclient ipykernel` to rebuild)

Content was drafted by one authoring pass per domain, then de-duplicated ("one concept, one
home") and cross-referenced. Expect to tweak entries as you learn — that's the point of the
matrix: the spreadsheet is the living source, Anki is just the drill.
