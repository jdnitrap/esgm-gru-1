# Graded MDBE Experiment (esgm-gru-1)

Sibling experiment derived from [jdnitrap/esgm-gru](https://github.com/jdnitrap/esgm-gru).
**This repo does not modify the original.** Local working copy of the original stayed at `/workspace/esgm-gru` untouched.

## Goal

1. Fix known `ASCII_Linguistics` / MDBE table bugs (Vowel/Consonant/Numeral/Punctuation).
2. Wire `NextByteRNN` so it can concatenate a learned `Embedding(256, emb_dim)` with **graded float** MDBE columns from the fixed CSV (not only binary frozen `byte_identity` edges).
3. Train a small next-byte model with vs without graded MDBE tags and report held-out **perplexity**.

## Change A — ASCII_Linguistics column fixes

### What was wrong / observed

`head.py` and `EXPERIMENT_LOG.md` already noted that `mdbe/ASCII_Linguistics.csv` Vowel/Consonant, Numeral, and Punctuation were wrong/scrambled; language_mechanics worksheets were OK and left alone.

Audit of both CSVs against `byte_identity.byte_categories()` / ASCII rules (`A-Z a-z` alpha; `0-9` numeral; `aeiouAEIOU` vowel else consonant among alphas; punctuation ranges matching byte_identity):

| File | Vowel mismatches | Consonant | Numeral | Punctuation |
|------|------------------|-----------|---------|-------------|
| `ASCII_Linguistics.csv` | 183 | 52 | 20 | 32 |
| `ASCII_Linguistics_v2.csv` | 29 | 52 | 20 | 32 |

Concrete examples (v2 before fix):

- `'A'` / `'a'` / `'E'` / `'e'`: **Vowel≈0.05**, Consonant≈0.78, **Numeral≈0.95** (vowels treated as consonants + high numeral).
- `'B'` / `'z'`: Consonant≈0.15, Vowel≈0.08 (letters not marked as consonants).
- Digits `'0'`/`'5'`: **Numeral≈0.05** (should be 1).
- `'!'` / `'.'`: **Punctuation≈0.01**, Vowel≈0.92 (punct marked as vowels).
- Space / many controls: high Vowel scores, not membership-correct.

Column-correlation check: truth **Vowel** matched the CSV **Numeral** column at **256/256** — strong evidence of a column scramble (Vowel values landed under Numeral), plus additional corruption of Punctuation/Consonant.

### Why fixed this way

- Structural membership columns must match deterministic ASCII rules (same as `byte_identity`), so they were **rewritten to clean 0/1** rather than attempting a partial unscramble of corrupted floats.
- Graded linguistic-role columns (Verb, Noun, …, Word Boundary, …) were **kept as floats** from v2 — those are soft alignment scores, not hard membership.
- Prefer v2 Character labels (NUL/SOH/…) and emit a clean `ASCII_Linguistics_fixed.csv` plus patched v1/v2 structural columns.

Vowel rule used: `aeiouAEIOU` → Vowel=1; other alphas → Consonant=1; non-letters → both 0.

### Where

- `mdbe/ASCII_Linguistics_fixed.csv` — preferred table for training (structural 0/1 + `is_*` extras + graded roles)
- `mdbe/ASCII_Linguistics_v2.csv` — structural columns corrected in place
- `mdbe/ASCII_Linguistics.csv` — structural columns corrected in place
- Notes: `docs/reasoning/01_ascii_linguistics_fix.md`

## Change B — GRU head reads graded MDBE floats

### What was wrong / observed

Original `NextByteRNN` only concatenated the learned embedding with binary tags from the graph/`byte_identity` path (`N_COLUMNS`). The spreadsheet path was deliberately avoided because of the bugs above. This experiment needs graded floats from the fixed CSV **without** requiring Hebbian graph memory.

### Why fixed this way

- Preserve MDBE design: rows = bytes 0–255; columns = named constraints; cells = floats.
- Keep tags-off baseline (embedding only) for a fair ablation.
- Do not require the graph for this training path.

### Where

- New `mdbe_table.py`: `load_mdbe_matrix(path) -> FloatTensor[256, n_cols]`, `mdbe_tags` / `mdbe_tags_batch`
- `head.py`: `NextByteRNN` / `NextByteHead` accept `tag_dim=` and `use_mdbe_table=`; when `use_mdbe_table=True`, tag width comes from the CSV matrix
- Notes: `docs/reasoning/02_graded_mdbe_head.md`

## Change C — Perplexity ablation

### Design

- **Corpus:** `dialogue_corpus.txt` (repo file, ~100KB ASCII Q/A); used first **80,000** bytes.
- **Model:** `NextByteRNN`, `emb_dim=32`, `hidden=64`, `seq_len=64`, `epochs=4`, `batch=32`, Adam `1e-3`, seed `0`, CPU.
- **MDBE:** embedding + 25 graded/structural columns from `ASCII_Linguistics_fixed.csv`.
- **Baseline:** embedding only (`use_tags=False`), same dims/data/steps.
- **Metric:** held-out next-byte perplexity = `exp(mean NLL)`; also accuracy.

### Results (reproduce with `python train_mdbe_ablation.py`)

| Variant | Held-out perplexity | Held-out accuracy |
|---------|---------------------|-------------------|
| **MDBE** (emb + graded tags) | **13.33** | **0.3059** |
| **Baseline** (emb only) | **15.22** | **0.2753** |

MDBE beats baseline on both perplexity and accuracy under matched conditions (1249 windows, 999 train / 250 held).

Raw JSON: `mdbe_ablation_results.json`. Notes: `docs/reasoning/03_perplexity_ablation.md`.

## Reproduce

```bash
# from repo root, with torch installed
python train_mdbe_ablation.py
```

## File list (this experiment)

| Path | Role |
|------|------|
| `mdbe/ASCII_Linguistics_fixed.csv` | Corrected graded MDBE table |
| `mdbe/ASCII_Linguistics_v2.csv` | Structural cols fixed |
| `mdbe/ASCII_Linguistics.csv` | Structural cols fixed |
| `mdbe_table.py` | Matrix loader + tag lookup |
| `head.py` | `tag_dim` / `use_mdbe_table` on RNN head |
| `train_mdbe_ablation.py` | Ablation trainer |
| `mdbe_ablation_results.json` | Latest numbers |
| `MDBE_GRADED_EXPERIMENT.md` | This writeup |
| `docs/reasoning/*.md` | Per-change reasoning notes |
| `dialogue_corpus.txt` | Training corpus sample |

Large graph JSON / checkpoints from the original were intentionally not published.
