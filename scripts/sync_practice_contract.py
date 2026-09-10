"""Sync the shared practice section without replacing repository instructions."""

from __future__ import annotations

import argparse
from pathlib import Path
import os


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- shared-practice:start -->"
END = "<!-- shared-practice:end -->"


def project(text: str, block: str) -> str:
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError("Expected zero or one complete shared-practice section")
    if START in text:
        start, end = text.index(START), text.index(END) + len(END)
        if end <= start:
            raise ValueError("Shared-practice markers are out of order")
        return text[:start] + block + text[end:]
    heading, separator, rest = text.partition("\n\n")
    if not separator:
        raise ValueError("AGENTS.md must have a heading and body")
    return heading + "\n\n" + block + "\n\n" + rest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--spider-root", type=Path, default=ROOT.parent / "spider")
    args = parser.parse_args()
    contract = (ROOT / "guidance/practice.md").read_text(encoding="utf-8").strip()
    block = (
        START + "\n"
        "<!-- Source: robotics-test-bench/guidance/practice.md. Refresh with "
        "scripts/sync_practice_contract.py from that repository. -->\n"
        + contract + "\n" + END
    )
    paths = [ROOT / "AGENTS.md", args.spider_root.resolve() / "AGENTS.md"]
    if paths[0].resolve() == paths[1].resolve():
        raise ValueError("Spider and the test bench must be distinct repositories")
    # Validate both targets before changing either file.
    plan = []
    for path in paths:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Expected a regular AGENTS.md: {path}")
        before = path.read_text(encoding="utf-8")
        plan.append((path, before, project(before, block)))
    drift = False
    for path, before, after in plan:
        if before == after:
            print(f"CURRENT {path}")
            continue
        drift = True
        if args.check:
            print(f"DRIFT {path}")
            continue
        temporary = path.with_name(path.name + ".practice-tmp")
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(after)
        os.replace(temporary, path)
        print(f"SYNCED {path}")
    return int(args.check and drift)


if __name__ == "__main__":
    raise SystemExit(main())
