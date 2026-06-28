# -*- coding: utf-8 -*-
"""CNN model and training entry point."""

import argparse
from pathlib import Path
from typing import Optional, Union

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

from CNN.data import load_emnist_letters


PathLike = Union[str, Path]
APP_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CHECKPOINT_DIR = APP_DIR / "artifacts" / "checkpoints"


class CNN:
    """The original network architecture, kept compatible with bundled weights."""

    def __init__(self, show_summary: bool = False):
        self.model = models.Sequential(
            [
                layers.Input(shape=(28, 28, 1)),
                layers.Conv2D(32, (5, 5), activation="relu", strides=(1, 1)),
                layers.MaxPooling2D((2, 2), padding="valid"),
                layers.Conv2D(64, (5, 5), activation="relu", strides=1),
                layers.MaxPooling2D((2, 2), padding="valid"),
                layers.Flatten(),
                layers.Dropout(0.25),
                layers.Dense(1024, activation="relu"),
                # EMNIST Letters labels are 1..26, so index 0 remains unused.
                layers.Dense(27, activation="softmax"),
            ],
            name="emnist_letters_cnn",
        )
        if show_summary:
            self.model.summary()


class DataSource:
    def __init__(self, data_dir: Optional[PathLike] = None):
        train_images, train_labels, test_images, test_labels = load_emnist_letters(
            data_dir=data_dir
        )
        self.train_images = train_images[..., np.newaxis].astype(np.float32) / 255.0
        self.test_images = test_images[..., np.newaxis].astype(np.float32) / 255.0
        self.train_labels = train_labels
        self.test_labels = test_labels


class PeriodicCheckpoint(tf.keras.callbacks.Callback):
    def __init__(self, directory: PathLike, every: int = 5):
        super().__init__()
        self.directory = Path(directory)
        self.every = every

    def on_epoch_end(self, epoch, logs=None):
        completed_epoch = epoch + 1
        if completed_epoch % self.every == 0:
            self.directory.mkdir(parents=True, exist_ok=True)
            path = self.directory / f"cp-{completed_epoch:04d}.ckpt"
            self.model.save_weights(str(path))
            print(f"\nSaved checkpoint: {path}")


class Train:
    def __init__(
        self,
        data_dir: Optional[PathLike] = None,
        checkpoint_dir: PathLike = DEFAULT_CHECKPOINT_DIR,
    ):
        self.cnn = CNN(show_summary=True)
        self.data = DataSource(data_dir=data_dir)
        self.checkpoint_dir = Path(checkpoint_dir)

    def train(self, epochs: int = 5):
        if epochs < 1:
            raise ValueError("epochs must be at least 1")

        self.cnn.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        save_callback = PeriodicCheckpoint(self.checkpoint_dir, every=min(5, epochs))
        self.cnn.model.fit(
            self.data.train_images,
            self.data.train_labels,
            epochs=epochs,
            callbacks=[save_callback],
        )
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        final_checkpoint = self.checkpoint_dir / f"cp-{epochs:04d}.ckpt"
        self.cnn.model.save_weights(str(final_checkpoint))
        print(f"Saved final checkpoint: {final_checkpoint}")

        _, accuracy = self.cnn.model.evaluate(
            self.data.test_images, self.data.test_labels, verbose=0
        )
        print(f"准确率：{accuracy:.4f}，共测试了 {len(self.data.test_labels)} 张图片")


def parse_args():
    parser = argparse.ArgumentParser(description="Train the EMNIST Letters CNN")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    trainer = Train(data_dir=args.data_dir, checkpoint_dir=args.checkpoint_dir)
    trainer.train(epochs=args.epochs)
