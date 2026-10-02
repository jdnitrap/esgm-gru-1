"""Launcher: unpacks packed experiment files then runs the real trainer."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
MARKER = ROOT / ".experiment_unpacked"

if not MARKER.exists():
    runpy.run_path(str(ROOT / "bootstrap_experiment.py"), run_name="__not_main__")
    MARKER.write_text("ok\n")

# After unpack, bootstrap overwrites this file with the real trainer.
# Re-exec the (now real) script.
runpy.run_path(str(Path(__file__).resolve()), run_name="__main__")
