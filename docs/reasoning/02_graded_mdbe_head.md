# Reasoning: Graded float MDBE head path

## Observed
NextByteRNN assumed tag_dim=N_COLUMNS from graph-backed build_tag_table(); spreadsheet path was avoided due to bugs.

## Decision
- mdbe_table.load_mdbe_matrix → [256, n_cols] floats indexed by raw byte.
- NextByteRNN(tag_dim=..., use_mdbe_table=True) concatenates Embedding + graded tags.
- Ablation training does not load graph.json / Hebbian memory.

## Why
Isolates the graded-table signal vs embedding-only under matched hyperparameters; preserves original graph tag path when tag_dim is left default.
