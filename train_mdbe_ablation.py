"""Stub: real trainer is packed. Run bootstrap first, or this auto-unpacks once."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
# If still a stub / tiny file, unpack packed essentials then re-exec
if ROOT.joinpath("mdbe/packed/train_mdbe_ablation.py.b64.gz.txt").exists():
    import bootstrap_experiment  # noqa: F401 — runs unpack on import? better call main

def _ensure():
    packed = ROOT / "mdbe" / "packed" / "train_mdbe_ablation.py.b64.gz.txt"
    if not packed.exists():
        raise SystemExit("missing packed trainer; clone incomplete")
    # Detect stub: our committed placeholder is tiny
    self_path = Path(__file__).resolve()
    if self_path.stat().st_size < 200:
        runpy.run_path(str(ROOT / "bootstrap_experiment.py"), run_name="__main__")
        # after unpack, re-exec the real module
        runpy.run_path(str(self_path), run_name="__main__")
        raise SystemExit(0)

if __name__ == "__main__":
    _ensure()
