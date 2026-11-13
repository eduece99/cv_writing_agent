---
description: Verify an output folder against project rules (page counts, claims, disclosure, comments)
agent: build
---
Run `python3 tools/check_outputs.py $1` — if no folder argument was given, run it on the newest `output/YYYYMMDD_HHMMSS/` folder.

Then: report every FAIL/WARN with its explanation, fix the causes (regenerate from `generate_documents.py` in that folder where applicable), re-run the checker until it passes, and update that run's `report.md` with what was fixed.
