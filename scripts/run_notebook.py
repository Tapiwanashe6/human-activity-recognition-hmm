"""Reproduce notebook analysis locally without modifying its source."""
from pathlib import Path
import json
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".run"
RUNTIME.mkdir(exist_ok=True)

for name in ["Human_Activity_Recordings.zip", "Test_Recordings.zip", "Continuous_Recording.zip"]:
    shutil.copy2(ROOT / "inputs" / name, RUNTIME / name)

notebook = json.loads((ROOT / "Human_Activity_HMM.ipynb").read_text())
namespace = {"__name__": "__main__", "display": lambda *items: [print(item) for item in items]}
plt.show = lambda *args, **kwargs: plt.close("all")
completed = 0

for index, cell in enumerate(notebook["cells"]):
    if cell["cell_type"] != "code":
        continue
    source = "".join(cell["source"])
    if "files.download(" in source:
        print(f"Skipping cell {index + 1}: Colab download only")
        continue
    source = source.replace("/content", str(RUNTIME))
    print(f"Running cell {index + 1}")
    exec(compile(source, f"notebook_cell_{index + 1}", "exec"), namespace)
    completed += 1

print(f"Completed {completed} analysis cells.")
print("Results:", RUNTIME / "activity_hmm")
