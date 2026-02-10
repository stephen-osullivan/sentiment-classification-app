# src/download_data.py
import logging
from pathlib import Path

import pandas as pd
from sklearn.datasets import fetch_openml

from sentiment.logging_config import setup_logging


def main():
    # setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    RAW_DATA_DIR = Path("data/raw")
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Downloading IMDB dataset from Hugging Face Datasets")
    from datasets import load_dataset

    dataset = load_dataset("imdb")

    train_df = dataset["train"].to_pandas()
    test_df = dataset["test"].to_pandas()

    logger.info(
        "Dataset downloaded with shape train: %s test : %s", 
        train_df.shape, test_df.shape)

    logger.info("Saving raw dataset to %s", RAW_DATA_DIR)
    train_df.to_csv(RAW_DATA_DIR / "imdb_train.csv", index=False)
    test_df.to_csv(RAW_DATA_DIR / "imdb_test.csv", index=False)

    logger.info("Download stage completed successfully")


if __name__ == "__main__":
    main()