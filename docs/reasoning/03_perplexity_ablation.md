# Reasoning: Perplexity ablation design

## Corpus choice
dialogue_corpus.txt is present in-repo (~100KB ASCII). Used first 80KB for a minutes-scale CPU run. Documented in train_mdbe_ablation.py / MDBE_GRADED_EXPERIMENT.md.

## Protocol
Same emb_dim/hidden/seq_len/epochs/batch/seed/data split for:
1. embedding + graded MDBE tags
2. embedding only

Metric: held-out next-byte perplexity = exp(mean NLL), plus accuracy.

## Result interpretation
MDBE held ppl 13.33 vs baseline 15.22 (acc 0.306 vs 0.275) after 4 epochs — graded tags help under this small-corpus regime. Not a claim about large-scale LLMs; an existence check that corrected graded columns are usable and improve small GRU next-byte modeling vs emb-only.
