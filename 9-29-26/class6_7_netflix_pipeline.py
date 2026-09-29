import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    drop_missing_rows,
    remove_duplicates,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # TODO 4:
    # Create a Path object from args.input.
    # Inside a try block, load that path using pd.read_csv().
    # Catch FileNotFoundError, log an ERROR message,
    # and exit with sys.exit(1).
    # Log an INFO message.
    path = Path(args.input)
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error(f"{path} not found")
        sys.exit(1)
    logger.info(f"{path} loaded {len(df)} rows and {len(df.columns)} columns")

    # TODO 5:
    # Call show_overview().
    # Log an INFO message.
    show_overview(df)
    logger.info("Dataframe overview displayed")

    # TODO 6:
    # Call remove_duplicates().
    # Call drop_missing_rows().
    # Log an INFO message after each step that
    # includes the number of rows removed.
    before = len(df)
    df = remove_duplicates(df)
    logger.info(f"{before - len(df)} duplicate rows removed")
    before = len(df)
    df = drop_missing_rows(df)
    logger.info(f"{before - len(df)} rows with missing values removed")

    show_overview(df, verbose = True)


if __name__ == "__main__":
    main()
