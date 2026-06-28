# CNN EMNIST

A TensorFlow CNN and PyQt desktop application for recognizing handwritten
English letters. The project uses the
[EMNIST Letters dataset](https://www.nist.gov/itl/products-and-services/emnist-dataset).

## Setup

```bash
git clone https://github.com/JiuChen0/CNN_EMINST.git
cd CNN_EMINST/CNN_EMNIST/GUI
conda env create -f environment.yml
conda activate cnn-emnist
```

No source-code paths need to be edited.

## Run the GUI

```bash
python GUI.py
```

The repository includes one pretrained checkpoint, so running the GUI does not
download the training dataset.

## Train the model

```bash
python -m CNN.train --epochs 5
```

On the first training run, the code downloads the official NIST archive
(approximately 536 MiB), verifies its checksum, extracts only the four EMNIST
Letters files (approximately 36 MiB), and deletes the full archive. Later runs
reuse the cached files.

The default data cache is:

- macOS: `~/Library/Caches/cnn-emnist/data`
- Linux: `~/.cache/cnn-emnist/data`
- Windows: `%LOCALAPPDATA%\cnn-emnist\data`

Set `CNN_EMNIST_DATA_DIR` to use a different location, or pass
`--data-dir PATH` to the training command. New checkpoints are written to
`CNN_EMNIST/GUI/artifacts/checkpoints` and are ignored by Git.

## Test

The lightweight tests do not download EMNIST or import TensorFlow:

```bash
python -m unittest discover -s tests -v
```

## Repository storage policy

Downloaded datasets, generated checkpoints, editor settings, build directories,
and packaged executables are excluded by `.gitignore`. Release binaries should
be attached to a GitHub Release instead of committed to the source repository.

Deleting these files in a new commit keeps future checkouts small, but their old
blobs remain in the existing Git history. Actually reducing the remote
repository size requires a one-time
[`git filter-repo` history rewrite](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#removing-files-from-a-repositorys-history)
and force-push. The old `GUI.exe` is a Git LFS object; GitHub documents that
[removed LFS objects continue to count toward storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage#git-lfs-objects-in-your-repository)
until the repository is recreated or GitHub Support purges them.
