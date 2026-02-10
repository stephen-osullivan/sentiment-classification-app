# src/download_data.py
import logging
from pathlib import Path

from datasets import load_dataset
import pandas as pd

from sentiment.logging_config import setup_logging
from sentiment.path_config import (
    RAW_DATA_DIR, RAW_TRAIN_DATA_PATH, RAW_TEST_DATA_PATH
)


def main():
    # setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Downloading IMDB dataset from Hugging Face Datasets")
    dataset = load_dataset("imdb")

    logger.info("Extracting train and test splits to pandas DataFrames")
    train_df = dataset["train"].to_pandas()
    test_df = dataset["test"].to_pandas()

    logger.info(
        "Dataset downloaded with shape train: %s test : %s", 
        train_df.shape, test_df.shape)

    logger.info("Saving raw dataset to %s", RAW_DATA_DIR)
    train_df.to_csv(RAW_TRAIN_DATA_PATH, index=False)
    test_df.to_csv(RAW_TEST_DATA_PATH, index=False)

    logger.info("Download stage completed successfully")


if __name__ == "__main__":
    main()