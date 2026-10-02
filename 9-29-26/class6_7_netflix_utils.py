import logging
import re
import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df, verbose = False):
    """Display basic information about a DataFrame."""
    # TODO 1:
    # Log a DEBUG message containing the shape.
    # Print the shape, first five rows, column names, and data types.
    logging.debug(f"shape: {df.shape}")
    if verbose == True:
        print(f"Shape: {df.shape}")
        # print(df.head())
        print(f"Columns: {list(df.columns)}")
        print(f"Data types: {df.dtypes}")


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    # TODO 2:
    # Remove exact duplicate rows.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.
    before = len(df)
    df = df.drop_duplicates()
    logging.debug(f"Removed {before - len(df)} duplicate row(s) from dataframe")
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    # TODO 3:
    # Drop rows containing one or more missing values.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.
    before = len(df)
    df = df.dropna()
    logging.debug(f"Removed {before - len(df)} duplicate row(s) from dataframe")
    return df


def clean_text(value):
    """Normalize one text value."""
    # TODO 1:
    # Strip surrounding whitespace.
    # Convert text to lowercase.
    # Collapse repeated whitespace.
    value = value.strip().lower()
    re.sub(r"\s+", " ", value)
    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    # Log an ERROR message and raise ValueError.
    # Calculate Q1, Q3, and IQR.
    # Use threshold to calculate lower and upper bounds.
    # Keep rows inside the bounds.
    # Log a DEBUG message containing the bounds and the number of rows removed.
    # Return the resulting DataFrame.
    try:
        df_original = df.copy()
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        df_cleaned = df[(df[column] >= lower) & (df[column] <= upper)]
        logging.debug(f"IQR bounding completed. Lower bound: {lower}. Upper bound: {upper}. \n"
                      f"Rows removed = {len(df_original) - len(df_cleaned)}")
        return df_cleaned
    except ValueError:
        logging.error(f"ValueError: {column} not in {df}")
        raise ValueError
