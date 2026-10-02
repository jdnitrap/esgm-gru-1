# Recommendations and tests — esgm-gru / esgm-gru-1

Sibling experiment notes for [jdnitrap/esgm-gru](https://github.com/jdnitrap/esgm-gru).
This file lives in **esgm-gru-1** only; the original repo was not modified.

## Context from this run

- Graded-MDBE ablation on `dialogue_corpus.txt` (~80KB, 4 epochs, CPU):
  - **MDBE** (embedding + graded tags): held-out perplexity **13.33**, accuracy **0.306**
  - **Baseline** (embedding only, no MDBE tags): held-out perplexity **15.22**, accuracy **0.275**
- Numbers also in `mdbe_ablation_results.json` / `MDBE_GRADED_EXPERIMENT.md`.
- **No `.pt` checkpoints** were kept.
- The experiment worker was **stopped early** on request; local work and a partial GitHub publish already existed at stop time.

## Recommended work / tests

### 1. Real benchmark harness

Add a real benchmark harness so every change gets measured against a baseline instead of living only in `EXPERIMENT_LOG.md`. Prefer a single script (or small suite) that prints comparable metrics (e.g. held-out perplexity / accuracy) for "before" vs "after" on a fixed corpus and seed.

### 2. Word- or token-level prediction

Try swapping the byte-level GRU for something that predicts at the **word or token** level. Bytes are a brutal unit to predict and may drown the memory's signal; a coarser output space would test whether Edge-State Graph Memory helps more when the generator isn't fighting next-byte entropy.

### 3. Stress-test Hebbian updates

Stress-test Hebbian updates with **noisy or shifting** input to see when the graph starts to fall apart (trust collapse, runaway weights, frozen-edge violations, contradiction storms). Record failure modes and thresholds next to the harness results.

### 4. Fix ASCII_Linguistics column bugs

Fix the known column bugs in `ASCII_Linguistics` (Vowel / Consonant / Numeral / Punctuation scrambled or wrong vs ASCII / `byte_identity` ground truth). In this sibling, that work landed as `mdbe/ASCII_Linguistics_fixed.csv` (and corrected structural columns on v1/v2); see `docs/reasoning/01_ascii_linguistics_fix.md`.

### 5. Head reads graded MDBE floats

Get the head actually reading **graded floats** from the MDBE tables instead of only the binary frozen edges from `byte_identity.py`, so the memory's nuance isn't thrown away. In this sibling: `mdbe_table.py` + `NextByteRNN(..., use_mdbe_table=True, tag_dim=…)` in `head.py`; notes in `docs/reasoning/02_graded_mdbe_head.md`.

### 6. Small-corpus next-byte perplexity vs no-memory baseline

Train on a small corpus and measure **next-byte perplexity** against a byte-level baseline with **no memory / no MDBE tags**. This run's result (above): MDBE **13.33** vs baseline **15.22**. Repro: `python train_mdbe_ablation.py`. Notes: `docs/reasoning/03_perplexity_ablation.md`.

## Suggested next steps (optional)

- Finish syncing any remaining local-only files to this remote if the tree still lags the box.
- Promote the ablation script into the harness in (1) with fixed seeds and a checked-in golden metric table.
- Do **not** push these experiment changes into the original `esgm-gru` unless that is requested separately.
