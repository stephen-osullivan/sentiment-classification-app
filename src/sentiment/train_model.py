# train model

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

import logging 

from sentiment.logging_config import setup_logging
from sentiment.path_config import PROCESSED_TRAIN_DATA_PATH, ARTIFACT_DIR, MODEL_PATH

def initialize_model() -> Pipeline:
    """
    Initialize and return a sentiment analysis model pipeline.
    """
    model = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=50_000,
                    ngram_range=(1, 2),
                    stop_words="english"
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                ),
            ),
        ]
    )
    return model


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Running model train logic")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    # load train data
    logger.info("loading processed train data")
    df = pd.read_csv(PROCESSED_TRAIN_DATA_PATH)
    X_train = df["text"]
    y_train = df["label"]

    # initialize and train model
    logger.info("initialising model")
    model = initialize_model()
    logger.info("training model")
    model.fit(X_train, y_train)
    # save the model
    logger.info("saving model to %s", MODEL_PATH)
    joblib.dump(model, MODEL_PATH)

    logger.info("Model saved!")

if __name__ == "__main__":
    main()