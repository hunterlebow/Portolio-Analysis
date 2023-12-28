import pandas as pd

# Function to merge data from two columns in a DataFrame that represent a ticker change.


def merge_ticker_change(df, old_ticker, new_ticker):
    """
    Merges data from two columns in a DataFrame that represent a ticker change.

    :param df: DataFrame with stock data.
    :param old_ticker: String, the column name of the old ticker.
    :param new_ticker: String, the column name of the new ticker.
    :return: DataFrame with the merged column.
    """

    # Combine the data from the old ticker and new ticker
    combined_data = df[old_ticker].combine_first(df[new_ticker])

    # Drop the old and new ticker columns from the original DataFrame
    df.drop([old_ticker, new_ticker], axis=1, inplace=True)

    # Add the combined data as a new column with the name of the new ticker
    df[new_ticker] = combined_data

    # Return the modified DataFrame
    return df
