import logging

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
