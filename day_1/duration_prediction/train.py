import argparse
from datetime import date
from loguru import logger

import pandas as pd
import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline


def read_dataframe(filename: str) -> pd.DataFrame:
    """
    Read and preprocess a parquet dataframe.

    Computes trip duration in minutes, filters trips between
    1 and 60 minutes, and converts location IDs to strings.

    Args:
        filename: Path to the parquet file.

    Returns:
        Preprocessed pandas DataFrame.
    """
    try:
        df = pd.read_parquet(filename)

        df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
        df.duration = df.duration.dt.total_seconds() / 60

        df = df[(df.duration >= 1) & (df.duration <= 60)]

        categorical = ["PULocationID", "DOLocationID"]
        df[categorical] = df[categorical].astype(str)
        return df
    except Exception as e:
        logger.exception(f"Could not get file: {filename}, error: {e}")
        raise e


def train(train_date: date, val_date: date, out_path: str) -> float:
    """
    Train a linear regression model on green taxi trip data.

    Downloads parquet data for the specified train and validation months,
    preprocesses it, trains a pipeline with a DictVectorizer and LinearRegression,
    evaluates RMSE on the validation set, and saves the trained model.

    Args:
        train_date (date): Month/year for the training data.
        val_date (date): Month/year for the validation data.
        out_path (str): File path to save the trained model (pickle).
    """
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet"
    train_url = base_url.format(year=train_date.year, month=train_date.month)
    val_url = base_url.format(year=val_date.year, month=val_date.month)
    df_train = read_dataframe(train_url)
    df_val = read_dataframe(val_url)
    logger.debug(f"df_train length is {len(df_train)}")
    logger.debug(f"df_val length is {len(df_val)}")

    categorical = ["PULocationID", "DOLocationID"]
    numerical = ["trip_distance"]

    train_dicts = df_train[categorical + numerical].to_dict(orient="records")
    val_dicts = df_val[categorical + numerical].to_dict(orient="records")

    target = "duration"
    y_train = df_train[target].values
    y_val = df_val[target].values

    dv = DictVectorizer()
    lr = LinearRegression()
    pipeline = make_pipeline(dv, lr)
    pipeline.fit(train_dicts, y_train)
    y_pred = pipeline.predict(val_dicts)

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"MSE is {mse}")

    with open(out_path, "wb") as f_out:
        pickle.dump(pipeline, f_out)
    return mse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model based on specified dates and save it to a given path")
    parser.add_argument("--train-date", required=True, help="Train month in the YYYY-MM format")
    parser.add_argument("--val-date", required=True, help="val month in the YYYY-MM format")
    parser.add_argument("--model-save-path", required=True, help="Path where the trained model should be saved.")
    
    args = parser.parse_args()
    train_year, train_month = args.train_date.split("-")
    val_year, val_month = args.val_date.split("-")

    train_date = date(int(train_year), int(train_month), 1)
    val_date = date(int(val_year), int(val_month), 1)
    out_path = args.model_save_path
    train(train_date=train_date, val_date=val_date, out_path=out_path)
