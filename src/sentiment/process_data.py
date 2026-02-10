# add something to remove the html
import re
from html import unescape

import logging
import pandas as pd

from sentiment.path_config import (
    RAW_DATA_DIR, RAW_TRAIN_DATA_PATH, RAW_TEST_DATA_PATH,
    PROCESSED_DATA_DIR, PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH
)
from sentiment.logging_config import setup_logging

def clean_text(text: str) -> str:
    HTML_TAG_RE = re.compile(r"<.*?>")
    # Convert to lowercase
    text = text.lower()
    # Decode HTML entities (e.g. &quot;)
    text = unescape(text)
    # Remove HTML tags
    text = re.sub(HTML_TAG_RE, " ", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def main():
    # setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # load data
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Loading raw data from %s", RAW_DATA_DIR)
    train_df = pd.read_csv(RAW_TRAIN_DATA_PATH)
    test_df = pd.read_csv(RAW_TEST_DATA_PATH)

    logger.info(
        "Raw data loaded with shape train: %s test : %s", 
        train_df.shape, test_df.shape)

    # clean data
    logger.info("Cleaning data text")
    train_df["text"] = train_df["text"].apply(clean_text)
    test_df["text"] = test_df["text"].apply(clean_text) 

    # save data
    logger.info("Saving processed training data to %s", PROCESSED_TRAIN_DATA_PATH)
    train_df.to_csv(PROCESSED_TRAIN_DATA_PATH, index=False)
    logger.info("Saving processed test data to %s", PROCESSED_TEST_DATA_PATH)
    test_df.to_csv(PROCESSED_TEST_DATA_PATH, index=False)

    logger.info("Data processing completed successfully")

if __name__ == "__main__":
    main()
