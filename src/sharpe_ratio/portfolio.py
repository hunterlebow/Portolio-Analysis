from datetime import datetime
import pandas as pd
from data_processing.polygon_api import Polygon


class Portfolio():
    def __init__(self, start_date: str, investments: list) -> None:
        """
        :param start_date: String, must be in YYYY-MM-DD format.  Do not recommend using start dates more than 5 years in the past.
        :param investments: List[String], list of stock tickers of the investments that will make up your portfolio.

        """
        self.START_DATE = start_date
        self.END_DATE = datetime.now().date().isoformat()
        self.investments = investments
        self.portfolio = pd.DataFrame()
        self.polygon = Polygon()
    

    def build_portfolio(self):
        for investment in self.investments:
            investment_data = self.polygon.get_investment_data(
                self.START_DATE,
                self.END_DATE,
                investment,
                self.polygon.get_api_key()
            )
            
            if investment_data is not None:
                self.portfolio[investment] = investment_data

        # TODO in this function:
        # Add the merge_ticker_change so it automatically happens here
        # Find data of all ticker changes and add it to /data
        # Implement automatic merges of the column so all the data is captured across...
        # ...all lifetime ticker names with the header being only the current ticker

    def clean_portfolio(self) -> None:
        self.portfolio.fillna(method='ffill', inplace=True)

    def to_excel(self, name) -> None:
        self.portfolio.to_excel(f"{name}.xlsx")
