# PAO & Multiple Encoding — starter kit

Learn the two ideas that power every matrix in this repo — **peg systems with multiple
encodings** and **PAO (Person-Action-Object)** — and master the spreadsheet workflow that
turns them into a trained skill.

**You need:** this README + `PAO_starter_blank.xlsx` (blank, with an `instructions` tab).
No prior memory training required.

---

## 1. Quick start (10 minutes)

1. Open `PAO_starter_blank.xlsx` → tab `digits_0-9`.
2. For each digit invent a **shape image** (what it *looks like*: 0 = wheel, 2 = swan…)
   and a **rhyme image** (what it *sounds like*: one-bun, two-shoe… or your own language).
3. Close your eyes, count 0→9 seeing the shapes, 9→0 hearing the rhymes. Done — you just
   used **two encodings on one address space**. Everything below is that idea, scaled up.

## 2. Core concepts

### 2.1 Peg system — fixed addresses

A peg system assigns a permanent, vivid image to every slot of a fixed address space
(digits 0-9, numbers 00-99, cards, the 000-999 Millenium). Learn the pegs ONCE; forever
after, anything you need to memorize gets *hung* on them. The spreadsheet's job is to make
the assignment explicit, collision-free, and trackable — one row per address.

### 2.2 The Major system — the phonetic encoding

Digits map to **consonant sounds**; vowels are free filler. You turn a number into
consonants, then into the first vivid word that fits:

| digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|-------|---|---|---|---|---|---|---|---|---|---|
| sound | s, z | t, d | n | m | r | l | j, ch, sh | k, hard g | f, v | p, b |

So 25 = n+l → *Nala, Nile, Nelly*; 40 = r+s → *rose, race*. This is the encoding behind
[`01.Millenium`](../01.Millenium/) (French variant, same table — see `millenium.ipynb`,
which literally greps a dictionary with these rules). The mapping is *generative*: you
never memorize arbitrary pairs, you **derive** them.

### 2.3 PAO — Person, Action, Object

Each number 00-99 gets a **Person** with a signature **Action** and **Object**
(23 = n+m → *Naomi (P) — modeling (A) — a mirror (O)*). The payoff is **compression**:

```
6 digits  =  Person(pair 1) + Action(pair 2) + Object(pair 3)  =  ONE scene
731942    →  the person of 73  doing the action of 19  with the object of 42
```

One image per 6 digits instead of per 2 — three times fewer palace loci, and the scenes
are unique combinations, so they never blur into each other. (Same trick works for cards:
see [`02.Cartes`](../02.Cartes/).)

### 2.4 Multiple encoding — why stack systems

One address, several independent retrieval routes:

| route | encoding | answers the question |
|-------|----------|----------------------|
| shape | visual | what does it *look* like? |
| rhyme | auditory | what does it *sound* like? |
| Major | phonetic | which consonants is it *made of*? |
| PAO | narrative | *who* does *what* with *which thing*? |
| palace | spatial | *where* did I put it? |

Memory research calls this dual/multiple coding: every extra route is a backup path — if
one cue fails during recall, another fires. The matrices in this repo *link* the routes in
one row: that linking, not any single trick, is what maximizes retention. (The
[`06.Programming_Millenium`](../06.Programming_Millenium/) matrix is the same principle
pointed at programming concepts: code = address, anchor scene = image, definition = payload.)

## 3. The spreadsheet IS the method

Every column exists for a memory-engineering reason (same schema across the repo):

| column | why it exists |
|--------|---------------|
| `Learned (0/1)` + `=SUM` row | binary progress tracking; the sum is your progress bar (the original Millenium sheet sits at 809/1000) |
| `Number` | the fixed address — never reorder, never renumber |
| `Person / Action / Object` | ONE canonical entry per address; ambiguity is the enemy |
| `Attention doublon / déjà pris` | collision registry — two addresses sharing an image WILL merge in memory; log every near-miss |
| `Non retenu mais convient` | the bench: good candidates you didn't keep, so you never re-evaluate from scratch |
| `Notes / Major sounds` | the derivation, so future-you can re-derive instead of re-memorize |

Workflow (also on the `instructions` tab):

```
fill one decade → Ctrl+F collision check → drill (F9 tab) → recall after 24h → Learned=1 → next decade
                                                                                    ↓
                                                              Anki export LAST, once stable
```

Anki is the drill engine, **not** the source of truth — you export *from* the matrix when
a block is stable (pipeline examples: `01.Millenium/tuto` tab, `06.Programming_Millenium/build.py`).

## 4. Template tour (`PAO_starter_blank.xlsx`)

| tab | what it's for |
|-----|---------------|
| `instructions` | the 9-step workflow + worked examples (25 = Nala; 731942 = one scene) |
| `digits_0-9` | your shape + rhyme images; Major consonants prefilled as reference |
| `pao_00-99` | the main matrix: 100 blank P/A/O rows, Major-sound hints prefilled, SUM row at the bottom |
| `drill` | press F9 → random 6-digit number; visualize the scene, then the VLOOKUPs reveal the answer |

## 5. Progression path

1. **Day 1:** `digits_0-9` (shape + rhyme).
2. **Weeks 1-4:** `pao_00-99`, one decade per session, drilling as you go.
3. **Then:** the 000-999 [`01.Millenium`](../01.Millenium/) (Major-system images), cards
   ([`02.Cartes`](../02.Cartes/)), and subject matrices like
   [`06.Programming_Millenium`](../06.Programming_Millenium/).

## 6. Pitfalls (read before filling row 1)

- **Vague beats nothing, vivid beats vague.** A person you can *see moving* — not "a doctor".
- **Don't change a peg after you start learning it.** Fix collisions *before* Learned=1;
  after that, the déjà-pris column exists precisely to stop you from "improving" pegs mid-flight.
- **Actions must be visibly different.** Running vs jogging will merge; running vs juggling won't.
- **Distinct persons.** Two bald men with glasses become one bald man with glasses.
- **Derive, don't invent.** If the Person doesn't come from the Major sounds, future-you
  can't reconstruct it after a lapse.
- **Don't rush to Anki.** Drilling unstable pegs burns wrong images in.

## 7. Regenerate the template

```bash
pip install openpyxl
python3 make_template.py   # rewrites PAO_starter_blank.xlsx
```
