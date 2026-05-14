#!/usr/bin/env python3
"""
convert_paper.py  --  bridge between proof_viz.exe and the Claude Code
                      /paper-to-lean skill.

Called by proof_viz.exe as:
    py -3 convert_paper.py  <pdf_path>  <output_lean_path>

Steps:
  1. Locate the repo root by walking up from this script until lakefile.toml is found.
  2. Run: claude -p "/paper-to-lean <pdf_path>" --dangerously-skip-permissions
     with cwd = repo root (so the .claude/commands/ skill is visible).
  3. Find the .lean file created/modified in Mathematics/.
  4. Copy it to <output_lean_path> so proof_viz.exe can load it.
"""

from __future__ import annotations

import glob
import os
import pathlib
import shutil
import subprocess
import sys


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
    if len(sys.argv) < 3:
        print("Usage: convert_paper.py <pdf_path> <output_lean_path>", file=sys.stderr)
        return 2

    pdf_path = os.path.abspath(sys.argv[1])
    output_lean_path = os.path.abspath(sys.argv[2])

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = find_repo_root(script_dir)
    if not repo_root:
        print("ERROR: Could not find repository root (no lakefile.toml found).", file=sys.stderr)
        return 1

    math_dir = os.path.join(repo_root, 'Mathematics')

    print(f"Repo root : {repo_root}")
    print(f"PDF input : {pdf_path}")
    print(f"Lean out  : {output_lean_path}")
    print(flush=True)

    # Snapshot existing .lean files so we can detect what is new after conversion.
    before: dict[str, float] = {
        f: os.path.getmtime(f)
        for f in glob.glob(os.path.join(math_dir, '*.lean'))
    }

    # Use forward slashes so bash / pdftotext inside the skill handles the path cleanly.
    pdf_fwd = pdf_path.replace('\\', '/')
    prompt = f'/paper-to-lean {pdf_fwd}'

    print("Running Claude Code /paper-to-lean skill ...", flush=True)
    print(f"  cwd: {repo_root}", flush=True)
    print(flush=True)

    # shell=True lets Windows resolve claude / claude.cmd from PATH correctly.
    cmd = f'claude -p "{prompt}" --dangerously-skip-permissions'
    result = subprocess.run(cmd, cwd=repo_root, shell=True)

    if result.returncode != 0:
        print(f"\nERROR: claude exited with code {result.returncode}", file=sys.stderr)
        return result.returncode

    # Find .lean files that are new or freshly modified.
    after: dict[str, float] = {
        f: os.path.getmtime(f)
        for f in glob.glob(os.path.join(math_dir, '*.lean'))
    }
    new_files = [
        f for f, t in after.items()
        if f not in before or t > before.get(f, 0) + 1.0
    ]

    if not new_files:
        print("ERROR: No new .lean file found in Mathematics/ after conversion.", file=sys.stderr)
        return 1

    generated = max(new_files, key=lambda f: after[f])
    shutil.copy2(generated, output_lean_path)

    print(f"\nGenerated : {generated}")
    print(f"Copied to : {output_lean_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
