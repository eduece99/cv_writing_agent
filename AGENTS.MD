# Agent pointers

## Current run

- Targeted role: **Staff Backend Engineer, Altium (Renesas Group)** (JD at `ref/job_description_altium.txt`, source https://renesas.dejobs.org/cambridge-gbr/staff-backend-engineer/F6BA8AF1917C454381A5A8DB66B23A26). Cambridge GBR **on-site**. Platform API/gateway/SDKs/MCP + Developer Center for "users and AI clients". C# preferred, Python/Golang/JS; Azure named as a cloud-plus (claimable); Docker/K8s/C#/Golang/SaaS/user-facing docs not claimed.
- Previous run same day: `output/20261116_151242/` (Benchling Solution Consultant – R&D, CV-only + ai_tools_summary.md — the AI summary is reusable for future applications). Older: `output/20261113_170500/` (Cresset), `output/20261113_165507/` (Molyon), `output/20261113_164945/` (Molyon, superseded).
- Candidate source: `ref/Profile.pdf` (updated 2026-11-13: Astex now "November 2023 – November 2026", location "Greater Cambridge Area").
- User confirmations: **no GCP experience** (never mention GCP in CV/letter); **German (basic) may be included**.
- Outputs: `output/YYYYMMDD_HHMMSS/` containing `cv.docx`, `cover_letter.docx` (unless letter-less), PDFs, `generate_documents.py` and `report.md`.

## Tooling (added 2026-11-13)

- **JD retrieval — dejobs.org sites (Renesas/Altium, DHI "JobSyn" platform)**: the job page is a Nuxt SPA; the full JD is at `https://microsites.dejobs.org/ALL_JOBS/{guid}.json` (guid from the URL). The search API (`prod-search-api.jobsyn.org/api/`) only serves `v1/complete/*` autocomplete. Ashby sites (Benchling): full JD is embedded in the page HTML as JSON-LD `JobPosting` — fetch with format html; the posting API returns 401.

- **OpenCode commands**: `/cv <JD url or pasted text>` (full application run), `/letter <job/revision>` (cover letter only), `/check [folder]` (run the verifier). Defined in `.opencode/commands/*.md` — the standard run procedure lives there, so new sessions follow it without improvisation.
- **`tools/docgen_common.py`** — shared generation helpers (`new_from_template`, `builder`, `set_text`, `first_rpr`, `apply_doubtful_comments`, `add_disclosure`, `convert_pdfs`). New `generate_documents.py` scripts should import this and contain only content + the proto-paragraph map (see its docstring).
- **`tools/check_outputs.py [folder]`** — post-run verifier: file existence, page counts (pdfinfo), forbidden-claims scan of the CV (FAIL) and letter (WARN), AI-disclosure presence, doubtful-item comment anchoring. Run after every generation; exit 1 on any FAIL.
- **`tools/doubtful.json`** — config for the checker (doubtful needles + comment texts, page limits, forbidden list). Edit there rather than in the script.
- `AGENTS.MD`, `.opencode/` and `tools/` are tracked in git; `output/` and `ref/` remain ignored.

## Working notes

- Generate from the supplied templates by editing them in place (clone styled paragraphs, replace runs) so the template page size, margins, fonts and paragraph styles are retained. Do not build from `Document()` from scratch — a previous run did that and had to be redone.
- CV bullets: `List Paragraph` style with `numId=2` (`ilvl=0` top level, `ilvl=1` nested). Publications use `numId=1`. Cover letter paragraphs use the `Texto preformateado` style — keep it (the 20261113 run did; earlier runs rendered it as 11pt TNR).
- The CV template is US Letter with narrow margins (about 0.51" left/right, 0.39" top, 0.315" bottom) and Times New Roman 12pt. Preserve this rather than forcing 1-inch margins.
- The CV template's contact lines contain hyperlinks. Clear the whole paragraph content except `w:pPr` before rebuilding the header, otherwise the hyperlink runs remain and duplicate the text.
- The cover letter template uses a 10pt monospace `Texto preformateado` style. It has been rendered as 11pt Times New Roman in the current output for a professional letter; note this as a deviation if repeated.
- LibreOffice is installed but needs `LD_LIBRARY_PATH=/usr/lib/libreoffice/program` to start on this machine:
  `LD_LIBRARY_PATH=/usr/lib/libreoffice/program soffice --headless --convert-to pdf --outdir . cv.docx cover_letter.docx`
- Doubtful (bio-unsupported) items must be flagged with Word comments directly on the CV, not just in the report — template-only content to check includes: degree classification "(First class)", PhD thesis title, Cabot Agile/Gantt bullet, Thames "subsequently promoted" clause, and the Non-Professional Activities line. All use `python-docx` `add_comment` on the run.
- The CV must end with the AI-assistance disclosure from the cv_writer skill, in 8–10pt: "This CV was generated with the use of an AI assistant (GLM, via OpenCode) and thereafter proof-read.  Please visit my github for details." (model name per the model actually used).
- `pdftotext -layout`, `pdfinfo` and `pdftohtml -xml` are available for layout checks. `python-docx` is installed (v1.2.0 — supports `Document.add_comment` for flagging doubtful CV items); PyMuPDF (`fitz`) is not.

## Candidate details and discrepancies to check

- Profile headline: Lead Software Developer; current role: **Lead Software Engineer, Astex Pharmaceuticals (UK), November 2023 – November 2026** (updated profile matches the template dates; resolved 2026-11-13).
- Profile languages: Spanish (Professional Working) plus German (basic) — both confirmed for inclusion by the user on 2026-11-13.
- The template says BSc Bioinformatics (First Class); `Profile.pdf` does not state the classification — still unverified; flagged with a Word comment in the latest outputs.
- Supported strengths: Python, C++, Java, JavaScript, SQL, R, Perl, Flask, Knockout.js, Oracle SQL/SQLAlchemy, Azure, Databricks, Synapse, Data Factory, PySpark, Spark NLP, GitLab CI, unit testing, code review, mentoring and stakeholder communication.
- Do **not** claim Docker, Kubernetes, Terraform, AWS, GCP, .NET, React, Node.js, microservices, serverless, FastAPI, Django, Vue.js, TypeScript or consulting experience without new evidence (JD technologies seen so far; transferability may be discussed honestly in the letter, e.g. "Flask → FastAPI/Django", "Azure → AWS").

## Project rules

- Do not invent skills, achievements or employment details. Flag uncertain items in the report and ask the user where needed.
- Produce a dated output folder with `cv.docx`, `cover_letter.docx`, `report.md` and the generation script. PDFs are useful extras.
- The report must cover inputs used, deviations from the templates, issues, assumptions, clarification needed, an alignment score (1–10), recommendations and a command log.
