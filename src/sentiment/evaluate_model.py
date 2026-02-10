# src/evaluate_model.py
import json
import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

from sentiment.path_config import (
    MODEL_PATH, PROCESSED_TEST_DATA_PATH, METRICS_PATH
)
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def main():
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Loading model from %s", MODEL_PATH)
    model = joblib.load(MODEL_PATH)

    logger.info("Loading test data")
    X_test = pd.read_csv(PROCESSED_TEST_DATA_PATH)["text"]
    y_test = pd.read_csv(PROCESSED_TEST_DATA_PATH)["label"]

    logger.info("Running predictions on %d samples", len(X_test))
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    report_dict = classification_report(
        y_test,
        y_pred,
        output_dict=True,
        zero_division=0,
    )

    metrics = {
        "accuracy": accuracy,
        "classification_report": report_dict,
    }

    # --- Logging (human-readable) ---
    logger.info("Accuracy: %.4f", accuracy)
    logger.info("Classification report:\n%s", classification_report(y_test, y_pred))

    # --- Persist metrics for DVC ---
    logger.info("Saving evaluation metrics to %s", METRICS_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info("Evaluation stage completed successfully")


if __name__ == "__main__":
    main()
