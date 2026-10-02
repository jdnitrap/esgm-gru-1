"""Unpack graded-MDBE experiment essentials from mdbe/packed/."""
from pathlib import Path
import gzip, base64, runpy

here = Path(__file__).resolve().parent
pack = here / "mdbe" / "packed"
mapping = {
    "train_mdbe_ablation.py.b64.gz.txt": "train_mdbe_ablation.py",
    "head.py.b64.gz.txt": "head.py",
    "dialogue_corpus_sample.txt.b64.gz.txt": "dialogue_corpus_sample.txt",
    "ASCII_Linguistics_fixed.b64.gz.txt": "mdbe/ASCII_Linguistics_fixed.csv",
    "ASCII_Linguistics_v2_fixed.b64.gz.txt": "mdbe/ASCII_Linguistics_v2.csv",
    "ASCII_Linguistics_fixed_v1.b64.gz.txt": "mdbe/ASCII_Linguistics.csv",
}
for src, dest in mapping.items():
    src_p = pack / src
    if not src_p.exists():
        print("skip missing", src); continue
    dest_p = here / dest
    dest_p.parent.mkdir(parents=True, exist_ok=True)
    dest_p.write_bytes(gzip.decompress(base64.b64decode(src_p.read_text().strip())))
    print("wrote", dest_p, dest_p.stat().st_size)
# also copy sample to dialogue_corpus.txt if missing
sample = here / "dialogue_corpus_sample.txt"
corp = here / "dialogue_corpus.txt"
if sample.exists() and not corp.exists():
    corp.write_bytes(sample.read_bytes())
    print("wrote", corp, "(from sample)")
print("done — run: python train_mdbe_ablation.py")
