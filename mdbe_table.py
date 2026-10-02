"""Load graded MDBE float tables (rows = bytes 0x00-0xFF) for the
NextByteRNN concat path.

Unlike byte_identity.py's binary frozen graph edges, these columns are
read from a corrected CSV (see mdbe/ASCII_Linguistics_fixed.csv) and
may be graded floats for linguistic-role columns, with 0/1 membership
for structural columns (Vowel/Consonant/Numeral/Punctuation/is_*).
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Optional, Sequence, Union

import torch

N_BYTES = 256
DEFAULT_MDBE_PATH = Path(__file__).resolve().parent / "mdbe" / "ASCII_Linguistics_fixed.csv"

# Columns used as graded (or 0/1) alignment tags for the ablation.
# Hex ASCII / Character are labels only; Frequency is kept as a soft prior.
DEFAULT_TAG_COLUMNS = [
    "Numeral",
    "Punctuation",
    "Consonant",
    "Vowel",
    "is_alpha",
    "is_digit",
    "is_upper",
    "is_punct",
    "is_space",
    "utf8_lead",
    # Graded linguistic-role soft scores from the spreadsheet (kept as floats)
    "Verb",
    "Subject",
    "Noun",
    "Adjective",
    "Adverb",
    "Conjunction",
    "Preposition",
    "Pronoun",
    "Article",
    "Auxiliary Verb",
    "Interjection",
    "Frequency",
    "Word Boundary",
    "Subword Start",
    "Subword End",
]


def load_mdbe_matrix(
    path: Union[str, Path] = DEFAULT_MDBE_PATH,
    columns: Optional[Sequence[str]] = None,
) -> tuple[torch.FloatTensor, List[str]]:
    """Load CSV -> FloatTensor [256, n_cols] indexed by byte value.

    Row labels must be hex token IDs `0x00`..`0xFF` (= decimal 0..255).
    Returns (matrix, column_names).
    """
    path = Path(path)
    cols = list(columns) if columns is not None else list(DEFAULT_TAG_COLUMNS)
    matrix = torch.zeros(N_BYTES, len(cols), dtype=torch.float32)
    seen = set()
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in cols if c not in reader.fieldnames]
        if missing:
            raise KeyError(f"{path} missing columns: {missing}")
        for row in reader:
            b = int(row["Hex ASCII"].strip(), 16)
            if not (0 <= b <= 255):
                raise ValueError(f"byte out of range: {row['Hex ASCII']}")
            seen.add(b)
            for j, c in enumerate(cols):
                matrix[b, j] = float(row[c])
    if len(seen) != N_BYTES:
        raise ValueError(f"{path} has {len(seen)} byte rows, expected 256")
    return matrix, cols


def mdbe_tags(
    byte_seq: Union[Sequence[int], torch.Tensor],
    matrix: torch.FloatTensor,
) -> torch.FloatTensor:
    """Look up graded tags for a byte sequence -> [seq, n_cols]."""
    if isinstance(byte_seq, torch.Tensor):
        idx = byte_seq.long()
        return matrix[idx]
    idx = torch.tensor(list(byte_seq), dtype=torch.long)
    return matrix[idx]


def mdbe_tags_batch(
    byte_batch: torch.Tensor,
    matrix: torch.FloatTensor,
) -> torch.FloatTensor:
    """byte_batch: [batch, seq] long -> [batch, seq, n_cols]."""
    return matrix[byte_batch.long()]
