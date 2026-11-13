---
description: Generate a tailored CV + cover letter application for a job (full run)
agent: build
---
Produce a complete job application (CV + cover letter), tailored to: $ARGUMENTS

Follow the project instructions in `.github/copilot-instructions.md` and `AGENTS.MD` exactly. Standard procedure:

1. **Prerequisite check** in `ref/`: `cv_template.docx`, `cl_template.docx`, `Profile.pdf`, and the job description (a file under `ref/`, or the URL/pasted text in the arguments). Ask the user for anything missing before proceeding.
2. **Load the skills**: invoke `cv_writer` and `cover_letter_writer` via the skill tool.
3. **Create the output folder** `output/YYYYMMDD_HHMMSS/` (current local datetime).
4. **Write `generate_documents.py`** in that folder, importing shared helpers from `tools/docgen_common.py`. Edit the templates in place (clone styled paragraphs, replace runs, keep `w:pPr`) so page size, margins, fonts, styles and list numbering are preserved. Never build from a blank `Document()`. Formatting notes for the templates are in `AGENTS.MD`.
5. **Content rules**: do not invent skills, achievements or employment details. Never claim Docker, Kubernetes, Terraform, AWS, GCP, .NET, React, Node.js, microservices, serverless, FastAPI, Django, Vue.js or TypeScript without user-provided evidence (honest transferability may be discussed once in the letter). Languages: Spanish (Professional Working), German (basic). Candidate details and standing user confirmations are in `AGENTS.MD`.
6. **Flag doubtful items**: every template-only, bio-unsupported claim gets a Word comment on the CV (python-docx `add_comment`). The needle list lives in `tools/doubtful.json`.
7. **AI disclosure**: end the CV with the disclosure line from `AGENTS.MD` in 8–10pt (use `tools/docgen_common.py`).
8. **Convert to PDF**: `LD_LIBRARY_PATH=/usr/lib/libreoffice/program soffice --headless --convert-to pdf --outdir <outdir> <outdir>/cv.docx <outdir>/cover_letter.docx`
9. **Verify**: run `python3 tools/check_outputs.py <outdir>` and fix every FAIL before reporting. CV must be ≤ 2 pages, letter exactly 1 page.
10. **Write `report.md`** (inputs used, deviations, issues, assumptions, clarification needed, alignment score 1–10, recommendations, command log) and **update `AGENTS.MD`** ("Current run" section).

If the arguments contain a URL, extract the job description from the web page first; if the page is a client-side app that cannot be scraped, ask the user to paste the text and save it to `ref/job_description.txt`.
