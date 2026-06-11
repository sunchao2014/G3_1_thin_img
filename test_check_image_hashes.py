from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from check_image_hashes import check_image_files, compute_md5_and_sha256


class CheckImageHashesTests(unittest.TestCase):
    def test_compute_md5_and_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "image.png"
            content = b"test-image-content"
            file_path.write_bytes(content)

            md5_value, sha256_value = compute_md5_and_sha256(file_path)

            self.assertEqual(md5_value, hashlib.md5(content).hexdigest())
            self.assertEqual(sha256_value, hashlib.sha256(content).hexdigest())

    def test_check_image_files_rejects_non_image_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "notes.txt"
            file_path.write_text("not an image", encoding="utf-8")

            with self.assertRaises(ValueError):
                check_image_files([file_path])


if __name__ == "__main__":
    unittest.main()
