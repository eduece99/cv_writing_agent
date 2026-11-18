#!/usr/bin/env python3
"""Verify a generated application folder against the project's standing rules.

Usage:  python3 tools/check_outputs.py [output/YYYYMMDD_HHMMSS]

Checks (config in tools/doubtful.json):
  1. cv.docx / cover_letter.docx exist; PDFs exist where the .docx does.
  2. Page counts: CV <= cv_max_pages, letter == letter_pages (pdfinfo).
  3. No forbidden-technology claims in the CV text (FAIL) — the letter may
     discuss transferability once, so letter hits are WARN with context.
  4. AI-assistance disclosure present at the end of the CV.
  5. Doubtful (bio-unsupported) needles present in the CV are anchored with a
     Word comment; needles legitimately absent are skipped.

Exit code 0 = pass, 1 = at least one FAIL.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from docx import Document

BASE = Path(__file__).resolve().parent.parent
CONFIG = json.loads((Path(__file__).resolve().parent / "doubtful.json").read_text())
WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def pdf_pages(pdf: Path):
    """Page count via pdfinfo, or None if the PDF is missing/unreadable."""
    if not pdf.exists():
        return None
    try:
        out = subprocess.run(
            ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
        ).stdout
        return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))
    except Exception:
        return None


def doc_text(path: Path) -> str:
    return "\n".join(p.text for p in Document(str(path)).paragraphs)


def comment_anchored_paragraphs(path: Path):
    """Paragraph texts of every paragraph carrying a w:commentReference."""
    anchored = []
    for p in Document(str(path)).paragraphs:
        if p._p.findall(f".//{WNS}commentReference"):
            anchored.append(p.text)
    return anchored


def scan(text: str, terms):
    """Return {term: matching line} for terms appearing in text."""
    hits = {}
    for term in terms:
        pattern = re.escape(term)
        if term == ".NET":
            pattern = r"\.NET\b"
        elif term in ("AWS", "GCP"):
            pattern = rf"{pattern}\b"
        m = re.search(pattern, text, re.I)
        if m:
            line = next(
                (ln for ln in text.splitlines() if term.lower() in ln.lower()), m.group(0)
            )
            hits[term] = line.strip()
    return hits


def check(outdir: Path, cv_only: bool = False) -> int:
    fails, warns = [], []

    def report(ok, msg):
        print(("PASS  " if ok else "FAIL  ") + msg)
        if not ok:
            fails.append(msg)

    print(f"=== check_outputs: {outdir.relative_to(BASE)} ===")

    # 1. files exist
    wanted = ["cv"] if cv_only else ["cv", "cover_letter"]
    for name in wanted:
        docx = outdir / f"{name}.docx"
        report(docx.exists(), f"{name}.docx exists")
        if docx.exists():
            pdf = outdir / f"{name}.pdf"
            if not pdf.exists():
                warns.append(f"{name}.pdf missing — run LibreOffice conversion")

    # 2. page counts
    if cv_only:
        cv_pages = pdf_pages(outdir / "cv.pdf")
        report(
            cv_pages is not None and cv_pages <= CONFIG["cv_max_pages"],
            f"cv.pdf pages: {cv_pages} (limit {CONFIG['cv_max_pages']})"
            if cv_pages is not None
            else "cv.pdf unreadable/missing — cannot verify page count",
        )
    else:
        cv_pages = pdf_pages(outdir / "cv.pdf")
        letter_pages = pdf_pages(outdir / "cover_letter.pdf")
        report(
            cv_pages is not None and cv_pages <= CONFIG["cv_max_pages"],
            f"cv.pdf pages: {cv_pages} (limit {CONFIG['cv_max_pages']})"
            if cv_pages is not None
            else "cv.pdf unreadable/missing — cannot verify page count",
        )
        report(
            letter_pages == CONFIG["letter_pages"],
            f"cover_letter.pdf pages: {letter_pages} (required {CONFIG['letter_pages']})"
            if letter_pages is not None
            else "cover_letter.pdf unreadable/missing — cannot verify page count",
        )

    # 3. forbidden claims
    cv_text = doc_text(outdir / "cv.docx") if (outdir / "cv.docx").exists() else ""
    for term, line in scan(cv_text, CONFIG["forbidden_in_cv"]).items():
        fails.append(f"forbidden claim in CV: {term!r}")
        print(f"FAIL  forbidden claim in CV: {term!r}  ({line[:80]})")
    if not scan(cv_text, CONFIG["forbidden_in_cv"]):
        report(True, "no forbidden-technology claims in the CV")

    letter_text = (
        doc_text(outdir / "cover_letter.docx")
        if (outdir / "cover_letter.docx").exists() and not cv_only
        else ""
    )
    letter_hits = scan(letter_text, CONFIG["warn_in_letter"])
    if letter_hits:
        for term, line in letter_hits.items():
            warns.append(f"{term!r} in letter (permitted as transferability — check wording)")
            print(f"WARN  {term!r} in letter, verify it is honest transferability: {line[:80]}")
    else:
        report(True, "no flagged technologies in the letter")

    # 4. AI disclosure
    disc = CONFIG["disclosure_needle"] in cv_text and CONFIG["disclosure_model"] in cv_text
    report(
        disc,
        "AI-assistance disclosure present in CV"
        if disc
        else "AI-assistance disclosure missing from the end of the CV",
    )

    # 5. doubtful-item comments
    anchored = comment_anchored_paragraphs(outdir / "cv.docx") if (outdir / "cv.docx").exists() else []
    for item in CONFIG["doubtful"]:
        needle = item["needle"]
        present = needle in cv_text
        commented = present and any(needle in p for p in anchored)
        if not present:
            print(f"SKIP  {needle[:40]!r}: not in this CV (nothing to flag)")
        else:
            report(
                commented,
                f"comment anchored on doubtful item {needle[:40]!r}"
                if commented
                else f"doubtful item {needle[:40]!r} is unflagged",
            )

    # summary
    print(f"\n{len(fails)} FAIL, {len(warns)} WARN")
    for w in warns:
        print("  warn:", w)
    return 1 if fails else 0


def main():
    cv_only = "--cv-only" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        outdir = Path(args[0])
    else:  # newest output/YYYYMMDD_HHMMSS folder
        dirs = sorted((BASE / "output").glob("[0-9]" * 8 + "_" + "[0-9]" * 6))
        if not dirs:
            print("no output folders found")
            return 1
        outdir = dirs[-1]
    if not outdir.is_absolute():
        outdir = BASE / outdir
    if not outdir.is_dir():
        print(f"not a directory: {outdir}")
        return 1
    return check(outdir, cv_only=cv_only)


if __name__ == "__main__":
    sys.exit(main())
