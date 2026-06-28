import gzip
import hashlib
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import numpy as np

from CNN.data import LETTERS_FILES, download_emnist_letters, load_emnist_letters


def write_idx_gzip(path: Path, values: np.ndarray):
    with gzip.open(path, "wb") as file:
        file.write(struct.pack(">BBBB", 0, 0, 8, values.ndim))
        file.write(struct.pack(f">{values.ndim}I", *values.shape))
        file.write(values.astype(np.uint8).tobytes())


class LoadEmnistLettersTest(unittest.TestCase):
    def test_reads_idx_files_without_fixed_dataset_shapes(self):
        with tempfile.TemporaryDirectory() as temporary:
            data_dir = Path(temporary)
            labels_train = np.array([1, 2], dtype=np.uint8)
            images_train = np.arange(2 * 28 * 28, dtype=np.uint8).reshape(2, 28, 28)
            labels_test = np.array([3], dtype=np.uint8)
            images_test = np.arange(28 * 28, dtype=np.uint8).reshape(1, 28, 28)
            files = (labels_train, images_train, labels_test, images_test)
            for filename, values in zip(LETTERS_FILES, files):
                write_idx_gzip(data_dir / filename, values)

            loaded = load_emnist_letters(data_dir=data_dir, download=False)

            expected = (images_train, labels_train, images_test, labels_test)
            for actual, values in zip(loaded, expected):
                np.testing.assert_array_equal(actual, values)

    def test_missing_data_has_actionable_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(FileNotFoundError, "download=True"):
                load_emnist_letters(data_dir=temporary, download=False)

    def test_download_extracts_only_letters_and_reuses_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_dir = root / "source"
            source_dir.mkdir()
            for index, filename in enumerate(LETTERS_FILES):
                write_idx_gzip(source_dir / filename, np.array([index], dtype=np.uint8))

            archive_path = root / "source.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                for filename in LETTERS_FILES:
                    archive.write(source_dir / filename, f"gzip/{filename}")
                archive.writestr("gzip/unrelated-split.gz", b"not needed")

            checksum = hashlib.md5(archive_path.read_bytes()).hexdigest()
            cache_dir = root / "cache"
            with (
                patch("CNN.data.EMNIST_URL", archive_path.as_uri()),
                patch("CNN.data.EMNIST_MD5", checksum),
            ):
                paths = download_emnist_letters(cache_dir)
                cached_paths = download_emnist_letters(cache_dir)

            self.assertEqual(paths, cached_paths)
            self.assertTrue(all(path.is_file() for path in paths))
            self.assertFalse((cache_dir / "emnist-gzip.zip").exists())
            self.assertFalse((cache_dir / "unrelated-split.gz").exists())


if __name__ == "__main__":
    unittest.main()
