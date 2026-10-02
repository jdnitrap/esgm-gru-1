# Reasoning: ASCII_Linguistics structural column fix

## Observed
- head.py documented scrambled Vowel/Consonant/Numeral/Punctuation in ASCII_Linguistics.csv.
- Audit vs byte_identity rules: hundreds of threshold mismatches; truth-Vowel == CSV-Numeral for all 256 rows in v2 (classic column scramble).
- Letters like A/e marked Numeral≈0.95 and Vowel≈0.05; punctuation marked Vowel≈0.92 and Punctuation≈0.01.

## Decision
Rewrite structural membership columns to deterministic 0/1 from ASCII rules; keep graded POS/role floats; add is_* columns aligned with byte_identity; ship ASCII_Linguistics_fixed.csv as the training table.

## Why not only unscramble
Partial column swap would fix Vowel←Numeral but Punctuation/Consonant remain inconsistent; ground-truth rewrite is auditable and matches byte_identity.
