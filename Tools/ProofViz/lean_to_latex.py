#!/usr/bin/env python3
"""
lean_to_latex.py  --  bridge between proof_viz.exe and the Claude Code
                      /lean-to-latex skill.

Called by proof_viz.exe as:
    py -3 lean_to_latex.py  <lean_input_file>  <latex_output_file>

Steps:
  1. Locate the repo root by walking up from this script until lakefile.toml is found.
  2. Run: claude -p "/lean-to-latex <lean_input_file>" --dangerously-skip-permissions
     with cwd = repo root (so the .claude/commands/ skill is visible).
     The skill writes LaTeX to <lean_input_file>.tex
  3. Compile the LaTeX to PDF via pdflatex, write <output_path_without_ext>.pdf
  4. Copy <lean_input_file>.tex to <latex_output_file> so proof_viz.exe can read it.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

LOG_PATH = os.path.join(
    os.environ.get('LOCALAPPDATA', tempfile.gettempdir()), 'ProofViz', 'lean_to_latex.log'
)


def log(msg: str) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)


def find_pdflatex() -> str | None:
    """Find pdflatex on PATH or in the default MiKTeX user install location."""
    p = shutil.which('pdflatex')
    if p:
        return p
    local = os.environ.get('LOCALAPPDATA', '')
    candidate = os.path.join(local, 'Programs', 'MiKTeX', 'miktex', 'bin', 'x64', 'pdflatex.exe')
    return candidate if os.path.isfile(candidate) else None


def render_pdf(tex_content: str, out_pdf: str) -> bool:
    """Wrap tex_content in a full document and compile to PDF via pdflatex."""
    pdflatex = find_pdflatex()
    log(f"pdflatex   : {pdflatex or 'NOT FOUND'}")
    if not pdflatex:
        return False

    document = (
        r'\documentclass[12pt]{article}' + '\n'
        r'\usepackage[margin=0.5cm,paperwidth=12cm,paperheight=20cm]{geometry}' + '\n'
        r'\usepackage{amsmath,amssymb,amsfonts}' + '\n'
        r'\pagestyle{empty}' + '\n'
        r'\begin{document}' + '\n'
        + tex_content + '\n'
        r'\end{document}'
    )

    # Use LOCALAPPDATA (long path) — GetTempPath returns 8.3 short paths
    # containing "~" which pdflatex interprets as a TeX command.
    latex_base = os.path.join(
        os.environ.get('LOCALAPPDATA', tempfile.gettempdir()), 'ProofViz', 'latex'
    )
    os.makedirs(latex_base, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='pvlatex_', dir=latex_base)
    try:
        tex_file = os.path.join(tmp, 'math.tex')
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(document)
        log(f"Compiling  : {tex_file}")
        result = subprocess.run(
            [pdflatex, '--enable-installer', '-interaction=nonstopmode',
             '-output-directory', tmp, tex_file],
            capture_output=True, timeout=90
        )
        log(f"pdflatex rc: {result.returncode}")
        if result.stderr:
            log(f"pdflatex err: {result.stderr.decode(errors='replace')[:500]}")
        pdf_file = os.path.join(tmp, 'math.pdf')
        exists = os.path.exists(pdf_file)
        log(f"PDF exists : {exists} -> {pdf_file}")
        if exists:
            shutil.copy2(pdf_file, out_pdf)
            log(f"Copied PDF : {out_pdf}")
            return True
        return False
    except Exception as e:
        log(f"pdflatex exception: {e}")
        return False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def find_repo_root(start: str) -> str | None:
    d = os.path.abspath(start)
    for _ in range(12):
        if os.path.exists(os.path.join(d, 'lakefile.toml')):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def main() -> int:
    log('=' * 60)
    log(f"lean_to_latex.py started, args={sys.argv[1:]}")
    log(f"PATH snippet: {os.environ.get('PATH','')[:200]}")

    if len(sys.argv) < 3:
        log("ERROR: wrong number of arguments")
        return 2

    lean_path = os.path.abspath(sys.argv[1])
    output_path = os.path.abspath(sys.argv[2])
    expected_tex = lean_path + '.tex'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = find_repo_root(script_dir)
    if not repo_root:
        log("ERROR: Could not find repository root (no lakefile.toml found).")
        return 1

    lean_fwd = lean_path.replace('\\', '/')
    prompt = f'/lean-to-latex {lean_fwd}'

    log(f"Repo root  : {repo_root}")
    log(f"Lean input : {lean_path}")
    log(f"LaTeX out  : {output_path}")
    log("Running Claude Code /lean-to-latex skill ...")

    cmd = f'claude -p "{prompt}" --dangerously-skip-permissions'
    result = subprocess.run(cmd, cwd=repo_root, shell=True)
    log(f"Claude rc  : {result.returncode}")

    if result.returncode != 0:
        log(f"ERROR: claude exited with code {result.returncode}")
        return result.returncode

    if not os.path.exists(expected_tex):
        log(f"ERROR: Expected output file not found: {expected_tex}")
        return 1

    shutil.copy2(expected_tex, output_path)
    log(f"Copied tex : {output_path}")

    try:
        with open(expected_tex, encoding='utf-8') as f:
            tex_content = f.read()
        out_pdf = os.path.splitext(output_path)[0] + '.pdf'
        log(f"PDF target : {out_pdf}")
        if render_pdf(tex_content, out_pdf):
            log("PDF render : SUCCESS")
        else:
            log("PDF render : FAILED (falling back to text display)")
    except Exception as e:
        log(f"PDF render skipped: {e}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
