from datetime import datetime
import pandas as pd
from data_processing.polygon_api import Polygon

class Portfolio():
    def __init__(self,start_date: str, end_date: str = datetime.now().date().isoformat()) -> None:
        """
        :param start_date: String, must be in YYYY-MM-DD format.  Do not recommend using start dates more than 5 years in the past.
        :param end_date: String, must be in YYYY-MM-DD format.  Default value is real time.
        :param investments: List[String], list of stock tickers of the investments that will make up your portfolio.

        """
        self.polygon = Polygon()
        self.START_DATE = start_date
        self.END_DATE = end_date
        self.investments = self._read_investments(file_name="investment_tickers.txt")
        self.index_funds = self._read_investments(file_name="indicies.txt")
        self.portfolio = pd.DataFrame()
        self.index_fund_portfolio = self.build_index_portfolio()

    

    def build_portfolio(self, ticker_updates:dict=None):                
        for investment in self.investments:
            investment_data = self.polygon.get_investment_data(
                self.START_DATE,
                self.END_DATE,
                investment,
                self.polygon.get_api_key()
            )
            
            if investment_data is not None:
                self.portfolio[investment] = investment_data
            
        if ticker_updates is not None and isinstance(ticker_updates, dict):
            for old_ticker, current_ticker in ticker_updates.items():
                self._handle_ticker_change(old_ticker, current_ticker)
              
        self._clean_portfolio()
            
    def build_index_portfolio(self):
        index_fund_portfolio = pd.DataFrame()
        
        for index_fund in self.index_funds:
            index_fund_data = self.polygon.get_indicie_data(
                self.START_DATE,
                self.END_DATE,
                index_fund,
                self.polygon.get_api_key()
            )
            
            if index_fund_data is not None:
                index_fund_portfolio[index_fund] = index_fund_data
        
        return index_fund_portfolio
        
    def _read_investments(self, file_name: str):
        with open(f"data/{file_name}", 'r') as file:
            tickers = file.readlines()

        # Optionally, strip the newline characters from each ticker
        tickers = [ticker.strip() for ticker in tickers]

        return tickers


    def _handle_ticker_change(self, old_ticker, current_ticker):
        """
        Merge data from one column into another and remove the original column.

        Parameters:
        df (pd.DataFrame): The DataFrame to operate on.
        col_to_remove (str): The name of the column whose non-null data is to be merged.
        col_to_keep (str): The name of the column to merge data into.

        Returns:
        pd.DataFrame: The DataFrame with the merged column.
        """
        #TODO Make sure ticker is valid... if not just continue
        #TODO Do this through looking at Polygons response to see if it was included in pflio build.
        
        # Copy non-null data from old_ticker to current_ticker
        self.portfolio.loc[self.portfolio[old_ticker].notnull(), current_ticker] = self.portfolio[old_ticker]
        
        # Drop the old_ticker column
        self.portfolio = self.portfolio.drop(columns=[old_ticker])


    def _clean_portfolio(self) -> None:
        total_na_values = self.portfolio.isna().sum().sum()
        print(f"Total missing values: {total_na_values}")
        if total_na_values > 0:
            na_rows = self.portfolio[self.portfolio.isna().any(axis=1)]
            print("Rows with missing values:")
            print(na_rows)
        
            self.portfolio.fillna(method='bfill', inplace=True)
            print(f"handled {na_rows.count} na values... all clean!")

    def to_excel(self, name) -> None:
        self.portfolio.to_excel(f"{name}.xlsx")
