import pandas as pd
import pytest

from class10_data_validator import validate_columns


@pytest.fixture # setup work
def sample_df():
    """Create a small DataFrame for testing."""
    return pd.DataFrame(
        {
            "title": ["Movie A", "Movie B"],
            "type": ["Movie", "Movie"],
            "release_year": [2020, 2021],
        }
    )


def test_validate_columns_with_valid_columns(sample_df):
    #  1:
    # Arrange the required column names.
    # Act by calling validate_columns().
    # Assert that the returned DataFrame has the expected columns.
    columns_list = sample_df.columns.to_list()
    df = validate_columns(sample_df, columns_list)
    assert sample_df.columns.to_list() == df.columns.to_list()

def test_validate_columns_with_missing_column(sample_df):
    # TODO 2:
    # Use pytest.raises() to confirm that validate_columns()
    # raises ValueError when a required column is missing.
    columns_list = ["title", "type", "release_year", "rating"]
    with pytest.raises(ValueError):
        validate_columns(sample_df, columns_list)
