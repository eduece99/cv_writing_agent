---
description: Generate or revise only the cover letter for a job (reuse an existing CV)
agent: build
---
Generate or revise the **cover letter only**, tailored to: $ARGUMENTS

Follow `.github/copilot-instructions.md`, `AGENTS.MD` and the `cover_letter_writer` skill (invoke it via the skill tool). Procedure:

1. If the arguments are a new job, do the prerequisite check first (`ref/cl_template.docx`, `ref/Profile.pdf`, job description — ask if missing). If revising an existing run, work from that run's folder and `report.md`.
2. Create `output/YYYYMMDD_HHMMSS/` (new run) or edit in place (revision), importing helpers from `tools/docgen_common.py`. Edit `ref/cl_template.docx` in place — keep its `Texto preformateado` paragraph style unless `AGENTS.MD` notes otherwise.
3. Content rules: nothing not supported by the bio; honest transferability for unclaimed technologies (Flask → FastAPI/Django, Azure → AWS) is allowed once; never claim Docker/AWS/GCP/GCP-listed tech as experience. Include the mandatory letter closing text from the skill.
4. Convert to PDF (`LD_LIBRARY_PATH=/usr/lib/libreoffice/program soffice --headless --convert-to pdf --outdir <outdir> <outdir>/cover_letter.docx`) and verify it is exactly 1 page with `tools/check_outputs.py <outdir>`.
5. Update `report.md` and `AGENTS.MD`.
