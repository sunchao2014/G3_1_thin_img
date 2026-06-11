#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"}


def is_image_file(file_path: Path) -> bool:
    return file_path.suffix.lower() in IMAGE_EXTENSIONS


def compute_md5_and_sha256(file_path: Path) -> tuple[str, str]:
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    with file_path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(8192), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)

    return md5_hash.hexdigest(), sha256_hash.hexdigest()


def check_image_files(file_paths: list[Path]) -> dict[Path, tuple[str, str]]:
    results: dict[Path, tuple[str, str]] = {}

    for file_path in file_paths:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not is_image_file(file_path):
            raise ValueError(f"Not an image file: {file_path}")
        results[file_path] = compute_md5_and_sha256(file_path)

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Check image files MD5 and SHA-256 hash.")
    parser.add_argument("files", nargs="+", help="Image file path(s) to check.")
    args = parser.parse_args()

    file_paths = [Path(file_name) for file_name in args.files]
    try:
        results = check_image_files(file_paths)
    except (FileNotFoundError, ValueError) as exc:
        print(exc)
        return 1

    for file_path, (md5_value, sha256_value) in results.items():
        print(f"{file_path}\n  MD5: {md5_value}\n  SHA256: {sha256_value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
