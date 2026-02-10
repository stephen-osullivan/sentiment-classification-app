# save paths
from pathlib import Path

# raw data
RAW_DATA_DIR = Path("data/raw")
RAW_TRAIN_DATA_PATH = RAW_DATA_DIR / "imdb_train.csv"
RAW_TEST_DATA_PATH = RAW_DATA_DIR / "imdb_test.csv"

# processed data
PROCESSED_DATA_DIR = Path("data/processed")
PROCESSED_TRAIN_DATA_PATH = PROCESSED_DATA_DIR / "imdb_train.csv"
PROCESSED_TEST_DATA_PATH = PROCESSED_DATA_DIR / "imdb_test.csv"

# artifacts
ARTIFACT_DIR = Path("artifacts")
MODEL_PATH = ARTIFACT_DIR / "sentiment_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "evaluation_metrics.json"