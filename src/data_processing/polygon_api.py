import requests
import pandas as pd
import os
from dotenv import load_dotenv


class Polygon():
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("POLYGON_API_KEY")

    def get_api_key(self):
        return self.API_KEY

    def get_investment_data(self, start_date, end_date, symbol, _api_key):
        """
        Fetches data for a single stock.

        :param start_date: The date .
        :param old_ticker: String, the column name of the old ticker.
        :param new_ticker: String, the column name of the new ticker.
        :return: DataFrame with the merged column.
        """

        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey={_api_key}"


        response = requests.get(url)
        data = response.json()

        # Check if the response contains the expected data
        if 'results' not in data:
            print(
                f"Error or unexpected format in response for {symbol}: {data}")
            return None

        df = pd.DataFrame(data['results'])
        df['date'] = pd.to_datetime(df['t'], unit='ms').dt.date
        df.set_index('date', inplace=True)
        df.rename(columns={'c': 'close'}, inplace=True)
        return df['close']


    def get_indicie_data(self, start_date, end_date, symbol, _api_key):
        """
        Fetches data for a single stock.

        :param start_date: The date .
        :param old_ticker: String, the column name of the old ticker.
        :param new_ticker: String, the column name of the new ticker.
        :return: DataFrame with the merged column.
        """

        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?sort=asc&limit=50000&apiKey={_api_key}"

        response = requests.get(url)
        data = response.json()

        # Check if the response contains the expected data
        if 'results' not in data:
            print(
                f"Error or unexpected format in response for {symbol}: {data}")
            return None

        df = pd.DataFrame(data['results'])
        df['date'] = pd.to_datetime(df['t'], unit='ms').dt.date
        df.set_index('date', inplace=True)
        df.rename(columns={'c': 'close'}, inplace=True)
        return df['close']
