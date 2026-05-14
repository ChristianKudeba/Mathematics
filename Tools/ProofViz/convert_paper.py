"""
convert_paper.py

ProofViz calls this script as:
    py -3 convert_paper.py input.pdf output.lean

Replace the `translate_pdf_to_lean` function with your real PDF-to-Lean
pipeline. The placeholder below creates a valid Lean file and, if the optional
`pypdf` package is installed, includes a short excerpt of extracted PDF text as
comments so you can verify that the app-to-script wiring works.
"""

from __future__ import annotations

import pathlib
import re
import sys
from datetime import datetime


def lean_comment_safe(text: str) -> str:
    """Avoid accidentally closing a Lean block comment."""
    return text.replace("-/", "- /")


def try_extract_pdf_text(pdf_path: pathlib.Path, max_chars: int = 6000) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return ""

    try:
        reader = PdfReader(str(pdf_path))
        chunks: list[str] = []
        for page in reader.pages[:5]:
            chunks.append(page.extract_text() or "")
            if sum(len(c) for c in chunks) >= max_chars:
                break
        text = "\n\n".join(chunks)
        return text[:max_chars]
    except Exception:
        return ""


def guess_name(pdf_path: pathlib.Path) -> str:
    stem = re.sub(r"[^A-Za-z0-9_]+", "_", pdf_path.stem).strip("_")
    if not stem:
        stem = "converted_paper"
    if stem[0].isdigit():
        stem = "paper_" + stem
    return stem


def translate_pdf_to_lean(pdf_path: pathlib.Path) -> str:
    """
    Placeholder translator.

    Put your real translation logic here, for example:
      1. extract PDF text/images,
      2. send theorem statements/proofs to an LLM or parser,
      3. emit Lean 4 code,
      4. optionally run `lake env lean` to check it.
    """
    name = guess_name(pdf_path)
    extracted = try_extract_pdf_text(pdf_path)

    lines = [
        "import Mathlib",
        "",
        f"/-!",
        f"Generated from: {lean_comment_safe(str(pdf_path))}",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "This is a placeholder output from convert_paper.py.",
        "Replace translate_pdf_to_lean() with your actual PDF-to-Lean pipeline.",
        "-/",
        "",
        f"namespace {name}",
        "",
    ]

    if extracted:
        lines.extend([
            "/-",
            "Extracted PDF text excerpt:",
            "",
            lean_comment_safe(extracted),
            "-/",
            "",
        ])
    else:
        lines.extend([
            "/-",
            "No PDF text was extracted. To test text extraction, install pypdf:",
            "  py -3 -m pip install pypdf",
            "-/",
            "",
        ])

    lines.extend([
        "-- TODO: replace these examples with translated theorem statements and proofs.",
        "theorem converted_placeholder : True := by",
        "  trivial",
        "",
        f"end {name}",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: convert_paper.py input.pdf output.lean", file=sys.stderr)
        return 2

    pdf_path = pathlib.Path(sys.argv[1]).resolve()
    out_path = pathlib.Path(sys.argv[2]).resolve()

    if not pdf_path.exists():
        print(f"input PDF does not exist: {pdf_path}", file=sys.stderr)
        return 1

    lean_code = translate_pdf_to_lean(pdf_path)
    out_path.write_text(lean_code, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
