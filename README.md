# esgm-gru-1 — Graded MDBE experiment sibling

Public experiment fork/sibling of [`jdnitrap/esgm-gru`](https://github.com/jdnitrap/esgm-gru).
**Does not replace or modify the original repo.**

This tree adds:
- Fixed `mdbe/ASCII_Linguistics_*.csv` structural columns + `ASCII_Linguistics_fixed.csv`
- `mdbe_table.py` + `NextByteRNN(..., use_mdbe_table=True, tag_dim=...)` graded float concat
- `train_mdbe_ablation.py` next-byte perplexity ablation (MDBE vs embedding-only)

See **[MDBE_GRADED_EXPERIMENT.md](MDBE_GRADED_EXPERIMENT.md)** for bugs found, fixes, and numbers.

## Quick start

```bash
python bootstrap_experiment.py   # unpack packed tables + train script + head + sample corpus
python train_mdbe_ablation.py    # needs torch; writes mdbe_ablation_results.json
```

Full original ESGM-GRU docs live in the sibling repo `jdnitrap/esgm-gru`.
Large graph JSON / checkpoints were intentionally omitted from this experiment publish.
