#!/usr/bin/env python3
"""Shared helpers for generate_documents.py runs in this project.

Every run edits ref/cv_template.docx and ref/cl_template.docx IN PLACE so the
template page size, margins, fonts, paragraph styles and list numbering are
preserved. Never build from a blank Document().

Typical per-run script:

    import sys; sys.path.insert(0, "<project>/tools")
    import docgen_common as dc

    doc, body = dc.new_from_template("<project>/ref/cv_template.docx")
    paras = doc.paragraphs                       # proto paragraphs (pre-clear)
    proto = {"name": paras[1], "jobhdr": paras[17], ...}
    add, _ = dc.builder(doc, body, proto)
    ... add("name", "EDMUND DUESBURY, PhD") etc. ...
    dc.apply_doubtful_comments(doc, DOUBTFUL)     # Word comments on the CV
    dc.add_disclosure(doc, add, "pub")            # AI-assistance line, 10pt
    doc.save(f"{OUT}/cv.docx")
    dc.convert_pdfs(OUT)
"""
import copy
import os
import subprocess
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

BASE = Path(__file__).resolve().parent.parent

DISCLOSURE_TEXT = (
    "This CV was generated with the use of an AI assistant ({model}) "
    "and thereafter proof-read.  Please visit my github for details."
)
DISCLOSURE_MODEL = "GLM, via OpenCode"  # update if the generating model changes

SOFFICE_ENV = dict(os.environ, LD_LIBRARY_PATH="/usr/lib/libreoffice/program")


def first_rpr(par):
    """Deep copy of the first run's rPr (run formatting), or None."""
    for r in par._p.findall(qn("w:r")):
        rpr = r.find(qn("w:rPr"))
        if rpr is not None:
            return copy.deepcopy(rpr)
    return None


def set_text(par, text, rpr=None):
    """Replace paragraph content, keeping w:pPr (style/numbering/margins)."""
    for child in list(par._p):
        if child.tag != qn("w:pPr"):
            par._p.remove(child)
    run = par.add_run()
    if rpr is not None:
        run._r.append(copy.deepcopy(rpr))
    run.text = text


def new_from_template(template_path):
    """Open a template and strip all its body paragraphs, keeping sectPr etc.

    Read the proto paragraphs from doc.paragraphs BEFORE calling this
    (deep-copy what you need first, or pass them to builder() beforehand).
    """
    doc = Document(str(template_path))
    body = doc.element.body
    for child in list(body):
        if child.tag == qn("w:p"):
            body.remove(child)
    return doc, body


def builder(doc, body, proto):
    """Return add(kind, text) that appends a clone of proto[kind] with text.

    proto maps kind -> a template paragraph (its pPr is cloned; rPr of its
    first run is applied to the new run so fonts survive).
    """
    rpr = {k: first_rpr(p) for k, p in proto.items()}

    def add(kind, text=""):
        p = body.makeelement(qn("w:p"), {})
        body.append(p)
        clone = copy.deepcopy(proto[kind]._p)
        body.replace(p, clone)
        if text:
            set_text(doc.paragraphs[-1], text, rpr.get(kind))
        return doc.paragraphs[-1]

    return add, rpr


def apply_doubtful_comments(cv, doubtful, author="CV Agent", initials="CV"):
    """Anchor a Word comment on every CV paragraph containing a doubtful needle.

    doubtful: iterable of (needle, comment_text). Returns the number added.
    The caller is responsible for saving the document afterwards.
    """
    added = 0
    for needle, ctext in doubtful:
        try:
            p = next(p for p in cv.paragraphs if needle in p.text)
            run = next((r for r in p.runs if needle in r.text), p.runs[0])
            cv.add_comment([run], text=ctext, author=author, initials=initials)
            added += 1
        except Exception as e:  # noqa: BLE001
            print(f"note: could not comment on {needle!r}: {e}")
    print(f"Word comments added: {added}/{len(list(doubtful))}")
    return added


def add_disclosure(cv, add, kind, size=10):
    """Append the AI-assistance disclosure in the given paragraph style/kind."""
    p = add(kind, DISCLOSURE_TEXT.format(model=DISCLOSURE_MODEL))
    for r in p.runs:
        r.font.size = Pt(size)
    return p


def convert_pdfs(outdir, names=("cv.docx", "cover_letter.docx")):
    """Convert the named .docx files to PDF next to themselves (LibreOffice)."""
    outdir = str(outdir)
    cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", outdir]
    cmd += [f"{outdir}/{n}" for n in names if (Path(outdir) / n).exists()]
    subprocess.run(cmd, check=True, env=SOFFICE_ENV)
