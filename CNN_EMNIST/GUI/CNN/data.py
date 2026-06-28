"""Download and load the EMNIST Letters dataset.

The official archive contains every EMNIST split. Only the four files needed
by this project are extracted, and the archive is removed afterwards.
"""

from __future__ import annotations

import gzip
import hashlib
import os
import shutil
import struct
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable, Optional, Tuple, Union

import numpy as np


EMNIST_URL = "https://biometrics.nist.gov/cs_links/EMNIST/gzip.zip"
EMNIST_MD5 = "58c8d27c78d21e728a6bc7b3cc06412e"
LETTERS_FILES = (
    "emnist-letters-train-labels-idx1-ubyte.gz",
    "emnist-letters-train-images-idx3-ubyte.gz",
    "emnist-letters-test-labels-idx1-ubyte.gz",
    "emnist-letters-test-images-idx3-ubyte.gz",
)

PathLike = Union[str, os.PathLike]


def default_data_dir() -> Path:
    """Return the platform cache directory, unless the user overrides it."""
    override = os.environ.get("CNN_EMNIST_DATA_DIR")
    if override:
        return Path(override).expanduser()

    if sys.platform == "darwin":
        cache_root = Path.home() / "Library" / "Caches"
    elif os.name == "nt":
        cache_root = Path(
            os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        )
    else:
        cache_root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return cache_root / "cnn-emnist" / "data"


def _md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download(url: str, destination: Path) -> None:
    """Download a URL atomically and print lightweight progress."""
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "CNN-EMNIST/1.0"})

    try:
        with (
            urllib.request.urlopen(request) as response,
            temporary.open("wb") as output,
        ):
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                downloaded += len(chunk)
                if total:
                    percent = downloaded * 100 // total
                    print(
                        f"\rDownloading EMNIST: {percent:3d}% "
                        f"({downloaded / 1024**2:.0f}/{total / 1024**2:.0f} MiB)",
                        end="",
                        flush=True,
                    )
        print()
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _extract_letters(
    archive_path: Path, data_dir: Path, filenames: Iterable[str]
) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        members = {Path(name).name: name for name in archive.namelist()}
        for filename in filenames:
            if filename not in members:
                raise RuntimeError(f"{filename} was not found in the EMNIST archive")

            target = data_dir / filename
            with archive.open(members[filename]) as source:
                with tempfile.NamedTemporaryFile(dir=data_dir, delete=False) as output:
                    temporary = Path(output.name)
                    shutil.copyfileobj(source, output)
            temporary.replace(target)


def download_emnist_letters(
    data_dir: Optional[PathLike] = None,
) -> Tuple[Path, ...]:
    """Download EMNIST once and return paths to the four Letters files."""
    directory = Path(data_dir).expanduser() if data_dir else default_data_dir()
    directory.mkdir(parents=True, exist_ok=True)
    paths = tuple(directory / filename for filename in LETTERS_FILES)
    missing = [path.name for path in paths if not path.is_file()]
    if not missing:
        return paths

    archive_path = directory / "emnist-gzip.zip"
    try:
        if not archive_path.is_file():
            print(f"EMNIST data was not found in {directory}.")
            print(
                "Downloading the official NIST archive (about 536 MiB, one time only)..."
            )
            _download(EMNIST_URL, archive_path)

        if _md5(archive_path) != EMNIST_MD5:
            archive_path.unlink(missing_ok=True)
            raise RuntimeError(
                "The EMNIST archive checksum does not match; please try again."
            )

        _extract_letters(archive_path, directory, missing)
    finally:
        # The full archive is much larger than the Letters split.
        archive_path.unlink(missing_ok=True)

    return paths


def _read_idx_gzip(path: Path) -> np.ndarray:
    with gzip.open(path, "rb") as file:
        header = file.read(4)
        if len(header) != 4:
            raise ValueError(f"Invalid IDX header in {path}")

        zero_a, zero_b, data_type, dimensions = struct.unpack(">BBBB", header)
        if (zero_a, zero_b, data_type) != (0, 0, 8):
            raise ValueError(f"Unsupported IDX format in {path}")

        shape_bytes = file.read(dimensions * 4)
        if len(shape_bytes) != dimensions * 4:
            raise ValueError(f"Invalid IDX shape in {path}")
        shape = struct.unpack(f">{dimensions}I", shape_bytes)
        values = np.frombuffer(file.read(), dtype=np.uint8)

    expected = int(np.prod(shape))
    if values.size != expected:
        raise ValueError(
            f"IDX payload in {path} has {values.size} values; expected {expected}"
        )
    return values.reshape(shape)


def load_emnist_letters(
    data_dir: Optional[PathLike] = None, download: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return ``x_train, y_train, x_test, y_test`` as uint8 arrays."""
    directory = Path(data_dir).expanduser() if data_dir else default_data_dir()
    paths = tuple(directory / filename for filename in LETTERS_FILES)

    if download:
        paths = download_emnist_letters(directory)
    elif not all(path.is_file() for path in paths):
        raise FileNotFoundError(
            f"EMNIST Letters data is missing from {directory}. "
            "Call load_emnist_letters(..., download=True) first."
        )

    y_train = _read_idx_gzip(paths[0])
    x_train = _read_idx_gzip(paths[1])
    y_test = _read_idx_gzip(paths[2])
    x_test = _read_idx_gzip(paths[3])
    return x_train, y_train, x_test, y_test
