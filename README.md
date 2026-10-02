# esgm-gru-1 — Graded MDBE experiment sibling

Public experiment fork/sibling of [`jdnitrap/esgm-gru`](https://github.com/jdnitrap/esgm-gru).
**Does not replace or modify the original repo.**

This tree adds:
- Fixed `mdbe/ASCII_Linguistics_*.csv` structural columns + `ASCII_Linguistics_fixed.csv`
- `mdbe_table.py` + `NextByteRNN(..., use_mdbe_table=True, tag_dim=...)` graded float concat
- `train_mdbe_ablation.py` next-byte perplexity ablation (MDBE vs embedding-only)

See **[MDBE_GRADED_EXPERIMENT.md](MDBE_GRADED_EXPERIMENT.md)** for bugs found, fixes, and numbers.

---

Full original ESGM-GRU README follows in HISTORY; see MDBE_GRADED_EXPERIMENT.md for this fork.

Clone of core modules is included for the graded-MDBE ablation. Large graph JSON omitted.
