#!/usr/bin/env python3
"""Generate immutable opam definitions for one allowlisted tagged release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "release-manifest.json").read_text())


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def package_opam(source_root: Path, package: str) -> Path:
    candidates = list(source_root.glob(f"{package}.opam"))
    if len(candidates) != 1:
        fail(f"expected exactly one {package}.opam in the release archive")
    return candidates[0]


def rewrite_opam(text: str, version: str, siblings: list[str], archive_url: str, checksum: str) -> str:
    if re.search(r"^url\s*\{", text, flags=re.MULTILINE):
        fail("source opam file already has a url stanza; release metadata must own it")
    version_line = f'version: "{version}"'
    if re.search(r"^version:\s*", text, flags=re.MULTILINE):
        text = re.sub(r"^version:\s*.*$", version_line, text, count=1, flags=re.MULTILINE)
    else:
        text = re.sub(r"^(opam-version:\s*.*)$", r"\1\n" + version_line, text, count=1, flags=re.MULTILINE)
    for sibling in siblings:
        text = re.sub(
            rf'"{re.escape(sibling)}"\s*(?:\{{[^}}]*\}})?',
            f'"{sibling}" {{= version}}',
            text,
        )
    return text.rstrip() + f'\n\nurl {{\n  src: "{archive_url}"\n  checksum: "sha256={checksum}"\n}}\n'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()

    if args.source not in MANIFEST:
        fail(f"source is not allowlisted: {args.source}")
    if not re.fullmatch(r"v[0-9][0-9A-Za-z.+~_-]*", args.tag):
        fail("tag must be v<opam-version>")
    if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
        fail("commit must be a full SHA-1")
    version = args.tag[1:]
    checksum = hashlib.sha256(args.archive.read_bytes()).hexdigest()
    archive_url = f"https://github.com/{args.source}/archive/{args.commit}.tar.gz"

    with tempfile.TemporaryDirectory() as directory:
        extracted = Path(directory)
        with tarfile.open(args.archive, "r:gz") as archive:
            archive.extractall(extracted, filter="data")
        roots = [path for path in extracted.iterdir() if path.is_dir()]
        if len(roots) != 1:
            fail("archive must contain one source root")
        for package in MANIFEST[args.source]:
            destination = ROOT / "packages" / package / f"{package}.{version}"
            if destination.exists():
                fail(f"package version already exists: {package}.{version}")
            destination.mkdir(parents=True)
            source = package_opam(roots[0], package)
            destination.joinpath("opam").write_text(
                rewrite_opam(source.read_text(), version, MANIFEST[args.source], archive_url, checksum)
            )
            print(destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
